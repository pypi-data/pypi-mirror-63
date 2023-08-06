import os
import random
import numpy as np
import scipy.interpolate as interp
from typing import List, Dict, Tuple

from resistics.common.base import ResisticsBase
from resistics.window.selector import WindowSelector
from resistics.transfunc.data import TransferFunctionData
from resistics.transfunc.io import TransferFunctionWriter
from resistics.common.io import checkAndMakeDir, fileFormatSampleFreq
from resistics.common.smooth import smooth1d
from resistics.regression.compute import spectralMatrices
from resistics.regression.robust import (
    sampleMAD0,
    hermitianTranspose,
    olsModel,
    chatterjeeMachler,
    mmestimateModel,
)


class LocalRegressor(ResisticsBase):
    """Performs single site (or intersite) transfer function calculations 

    By default, the LocalRegression is setup to calculate the impedance tensor using Hx, Hy as input channels and Ex, Ey as output channels. To calculate the Tipper, the appropriate input and output channels have to be set.

    Attributes
    ----------
    winSelector : WindowSelector
        A window selector object which defines which windows to use in the linear model
    decParams : DecimationParameters
        DecimationParameters object with information about the decimation scheme
    winParams : WindowParameters
        WindowParameters object with information about the windowing
    outpath : str 
        Location to put the calculated transfer functions (Edi files)
    inSite : str 
        The site to use for the input channels 
    inChannels: List[str] (["Hx", "Hy"])
        List of hannels to use as input channels for the linear system
    inSize : int 
        Number of input channels
    outSite : str 
        The site to use for the output channels
    outChannels : List[str] (["Ex", "Ey"])
        List of channels to use as output channels for the linear system
    outSize : int
        Number of output channels
    allChannels : List[str] 
        inChannels and outChannels combined into a single list
    crossChannels : List[str] 
        The channels to calculate the cross spectra out for
    intercept : bool (default False)
        Flag for including an intercept (static) term in the linear system
    method : str (options, "ols", "cm") 
        String for describing what solution method to use
    win : str (default hanning)
        Window function to use in robust solution
    winSmooth : int (default -1)
        The size of the window smoother. If -1, this will be autocalculated based on data size
    postpend : str (default "")
        String to postpend to the output filename to help file management
    evalFreq : List[float] or np.ndarray
        The evaluation frequencies
    impedances : List
    variances : List

    Methods
    -------
    __init__(proj, winSelector, outpath)
        Initialise with a Project instance and MaskData instance
    setInput(inSite, inChannels)
        Set the input site and channels
    setOutput(outSite, outChannels)
        Set the output site and channels
    process()
        Process the spectra to calculate the transfer function
    getWindowSmooth()
        Get the window smooth length
    checkForBadValues(numWindows, data)
        Check the spectral data for bad values that might cause an error   
    prepareLinearEqn(data)
        Prepare regressors and observations for regression from cross-power data
    robustProcess(numWindows, obs, reg)      
        Robust regression processing   
    olsProcess(numWindows, obs, reg)      
        Ordinary least squares processing
    stackedProcess(data)
        Stacked processing                  
    printList()
        Class status returned as list of strings
    """

    def __init__(self, winSelector: WindowSelector, outpath: str):
        """Intialise the processor

        Parameters
        ----------
        winSelector : WindowSelector
            A window selector instance
        outpath : str
            The path to write the transfer function data to
        """
        self.winSelector = winSelector
        self.decParams = winSelector.decParams
        self.winParams = winSelector.winParams
        self.outpath: str = outpath
        # default parameters for user options
        self.inSite: str = "dummy"
        self.inChannels: List[str] = ["Hx", "Hy"]
        self.inSize: int = len(self.inChannels)
        self.outSite: str = "dummy"
        self.outChannels: List[str] = ["Ex", "Ey"]
        self.outSize: int = len(self.outChannels)
        self.allChannels: List[str] = self.inChannels + self.outChannels
        self.crossChannels: List[str] = self.allChannels
        # solution options
        self.intercept: bool = False
        self.method: str = "cm"
        # smoothing options
        self.win: str = "hanning"
        self.winSmooth: int = 9
        # output filename
        self.postpend: str = ""
        # evaluation frequency data
        self.evalFreq = []
        self.impedances = []
        self.variances = []

    def setInput(self, inSite: str, inChannels: List[str]) -> None:
        """Set information about input site and channels
    
        Parameters
        ----------
        inSite : str
            Site to use for input channel data
        inChannels : List[str]
            Channels to use as the input in the linear system
        """
        self.inSite = inSite
        self.inChannels = inChannels
        self.inSize = len(inChannels)
        # set all and cross channels
        self.allChannels = self.inChannels + self.outChannels
        self.crossChannels = self.allChannels

    def setOutput(self, outSite: str, outChannels: List[str]) -> None:
        """Set information about output site and channels
    
        Parameters
        ----------
        inSite : str
            Site to use for output channel data
        inChannels : List[str]
            Channels to use as the output in the linear system
        """
        self.outSite = outSite
        self.outChannels = outChannels
        self.outSize = len(outChannels)
        # set all and cross channels
        self.allChannels = self.inChannels + self.outChannels
        self.crossChannels = self.allChannels

    def process(self, ncores: int = 0) -> None:
        """Process spectra data

        The processing sequence for each decimation level is as below:

        1. Get shared (unmasked) windows for all relevant sites (inSite and outSite)
        2. For shared unmasked windows
            
            - Calculate out the cross-power spectra.
            - Interpolate calculated cross-power data to the evaluation frequencies for the decimation level.
        
        3. For each evaluation frequency
            
            - Do the robust processing to calculate the transfer function at that evaluation frequency.

        The spectral power data is smoothed as this tends to improve results. The smoothing can be changed by setting the smoothing parameters. This method is still subject to change in the future as it is an area of active work
        """
        numLevels: int = self.decParams.numLevels
        for declevel in range(0, numLevels):
            self.printText("Processing decimation level {}".format(declevel))
            numWindows = self.winSelector.getNumSharedWindows(declevel)
            unmaskedWindows = self.winSelector.getUnmaskedWindowsLevel(declevel)
            numUnmasked = len(unmaskedWindows)
            self.printText(
                "Total shared windows for decimation level = {}".format(numWindows)
            )
            self.printText(
                "Total unmasked windows for decimation level = {}".format(numUnmasked)
            )
            if numUnmasked == 0:
                self.printText(
                    "No unmasked windows found at this decimation level ({:d}), continuing to next level".format(
                        declevel
                    )
                )
                continue
            self.printText("{} windows will be processed".format(numUnmasked))

            # set variables
            evalFreq = self.decParams.getEvalFrequenciesForLevel(declevel)
            totalSize: int = self.inSize + self.outSize
            numEvalFreq: int = len(evalFreq)
            dataSize: int = self.winSelector.getDataSize(declevel)
            smoothLen: int = self.getWindowSmooth(datasize=dataSize)
            # data array for each evaluation frequency and keep spectral power information for all windows
            evalFreqData: np.ndarray = np.empty(
                shape=(numEvalFreq, numWindows, totalSize, totalSize), dtype="complex"
            )

            # global to local map to help choose windows for each evaluation frequency
            localWin: int = 0
            global2local: Dict = {}
            # process spectral batches
            spectraBatches = self.winSelector.getSpecReaderBatches(declevel)
            numBatches = len(spectraBatches)
            for batchIdx, batch in enumerate(spectraBatches):
                # find the unmasked batched windows and add the data
                batchedWindows = unmaskedWindows.intersection(
                    set(range(batch["globalrange"][0], batch["globalrange"][1] + 1))
                )
                self.printText(
                    "Processing batch {:d} of {:d}: Global window range {:d} to {:d}, {:.3%} of data".format(
                        batchIdx + 1,
                        numBatches,
                        batch["globalrange"][0],
                        batch["globalrange"][1],
                        len(batchedWindows) / numUnmasked,
                    )
                )

                # collect spectrum data and compute spectral matrices
                # set batchedWindows from return to ensure proper order
                inReader = batch[self.inSite]
                inData, batchedWindows = inReader.readBinaryBatchGlobal(
                    globalIndices=batchedWindows
                )
                if self.outSite != self.inSite:
                    outReader = batch[self.outSite]
                    outData, _gIndicesOut = outReader.readBinaryBatchGlobal(
                        globalIndices=batchedWindows
                    )
                else:
                    outData = inData

                out = spectralMatrices(
                    ncores,
                    inData,
                    outData,
                    self.inChannels,
                    self.outChannels,
                    smoothLen,
                    self.win,
                    evalFreq,
                )

                for batchWin, globalWin in enumerate(batchedWindows):
                    evalFreqData[:, localWin] = out[batchWin]
                    # local to global map and increment local window
                    global2local[globalWin] = localWin
                    localWin = localWin + 1

            # close spectra files for decimation level
            for batch in spectraBatches:
                for site in self.winSelector.sites:
                    batch[site].closeFile()

            # data has been collected for each evaluation frequency, perform robust processing
            for eIdx in range(0, numEvalFreq):
                self.printText(
                    "Processing evaluation frequency = {:.6f} [Hz], period = {:.6f} [s]".format(
                        evalFreq[eIdx], 1 / evalFreq[eIdx]
                    )
                )
                # get the constrained windows for the evaluation frequency
                evalFreqWindows = self.winSelector.getWindowsForFreq(declevel, eIdx)
                if len(evalFreqWindows) == 0:
                    # no windows meet constraints
                    self.printText("No windows found - possibly due to masking")
                    continue
                localWinIndices = []
                for iW in evalFreqWindows:
                    localWinIndices.append(global2local[iW])

                self.printText(
                    "{:d} windows will be solved for".format(len(localWinIndices))
                )
                # restrict processing to data that meets constraints for this evaluation frequency
                self.evalFreq.append(evalFreq[eIdx])
                # solution using all components
                numSolveWindows, obs, reg = self.prepareLinearEqn(
                    evalFreqData[eIdx, localWinIndices]
                )
                out, var = self.robustProcess(numSolveWindows, obs, reg)
                # out, var = self.olsProcess(numSolveWindows, obs, reg)
                # out, var = self.stackedProcess(evalFreqData[eIdx, localWinIndices])
                self.impedances.append(out)
                self.variances.append(var)

        if len(self.evalFreq) == 0:
            self.printWarning(
                "No data was found at any decimation level for insite {}, outsite {} and specdir {}".format(
                    self.inSite, self.outSite, self.winSelector.specdir
                )
            )
            return

        # write out all the data
        self.writeTF(
            self.winSelector.specdir,
            self.postpend,
            self.evalFreq,
            self.impedances,
            self.variances,
        )

    def getWindowSmooth(self, **kwargs):
        """Window smoothing length

        Power spectra data is smoothed. This returns the size of the smoothing window.
    
        Parameters
        ----------
        datasize : int
            The size of the data

        Returns
        -------
        smoothLen : int
            Smoothing size
        """
        # check if window size specified by user
        if self.winSmooth != -1 and self.winSmooth > 1:
            return self.winSmooth
        # if not, calculate based on datasize
        if "datasize" in kwargs:
            winSmooth = kwargs["datasize"] * 1.0 / 16.0
            if winSmooth < 3:
                return 3  # minimum smoothing
            # otherwise round to nearest odd number
            winSmooth = np.ceil(winSmooth) // 2  # this is floor division
            return int(winSmooth * 2 + 1)
        # otherwise, return a default value
        return 15

    def checkForBadValues(self, numWindows: int, data: np.ndarray):
        """Check data for bad values and remove
        
        Parameters
        ----------
        numWindows : int
            The number of windows
        data : np.ndarray 
            Cross-spectra data

        Returns
        -------
        numGoodWindows : int
            The number of good windows
        goodData : np.ndarray
            The cross-spectra data with bad windows removed
        """
        finiteArray = np.ones(shape=(numWindows))
        for iW in range(0, numWindows):
            if not np.isfinite(data[iW]).all():
                finiteArray[iW] = 0
        numGoodWindows = sum(finiteArray)
        if numGoodWindows == numWindows:
            return numWindows, data
        self.printWarning(
            "Bad data found...number of windows reduced from {} to {}".format(
                numWindows, numGoodWindows
            )
        )
        goodWindowIndices = np.where(finiteArray == 1)
        return numGoodWindows, data[goodWindowIndices]

    def prepareLinearEqn(self, data: np.ndarray):
        r"""Prepare data as a linear equation for the robust regression

        This prepares the data for the following type of solution,

        .. math::
            y = Ax,

        where :math:`y` is the observations, :math:`A` is the regressors and :math:`x` is the unknown. 

        The number of observations is number of windows * number of cross-power channels
        The shapes of the arrays are as follows:
        
            - y is (number of output channels, number of observations)
            - A is (number of output channels, number of observations, number of input channels)
            - x is (number of output channels, number of input channels)

        Consider the impedance tensor,

        .. math::
            :nowrap:

            \begin{eqnarray}
            E_x & = & Z_{xx} H_x + Z_{xy} H_y \\
            E_y & = & Z_{yx} H_x + Z_{yy} H_y 
            \end{eqnarray}  

        Here, there are two input channels, :math:`H_x`, :math:`H_y` and two output channels :math:`E_x` and :math:`E_y`. In total, there are four components of the unknown impedance tensor, :math:`Z_{xx}`, :math:`Z_{xy}`, :math:`Z_{yx}`, :math:`Z_{yy}` (number of input channels * number of output channels). The number of observations is the number of windows multiplied by the number of channels used for cross-power spectra.     

        Parameters
        ----------
        data : np.ndarray
            Cross-power spectral data at evaluation frequencies

        Returns
        -------
        numWindows : int
            The number of windows included in the regression (after bad value removal)
        obs : np.ndarray
            Observations array
        reg : np.ndarray 
            Regressors array
        """
        numWindows = data.shape[0]
        # check for bad values
        numWindows, data = self.checkForBadValues(numWindows, data)
        crossSize = len(self.crossChannels)
        # for each output variable, have number of input regressor variables
        # construct our arrays
        obs = np.empty(shape=(self.outSize, crossSize * numWindows), dtype="complex")
        reg = np.empty(
            shape=(self.outSize, crossSize * numWindows, self.inSize), dtype="complex"
        )
        for iW in range(0, numWindows):
            iOffset = iW * crossSize
            for i in range(0, self.outSize):
                for j, crossChan in enumerate(self.crossChannels):
                    # this is the observation row where i is the observed output
                    crossIndex = self.allChannels.index(crossChan)
                    obs[i, iOffset + j] = data[iW, self.inSize + i, crossIndex]
                    for k in range(0, self.inSize):
                        reg[i, iOffset + j, k] = data[iW, k, crossIndex]
        return numWindows, obs, reg

    def robustProcess(
        self, numWindows: int, obs: np.ndarray, reg: np.ndarray
    ) -> Tuple[np.ndarray]:
        """Robust regression processing

        Perform robust regression processing using observations and regressors for a single evaluation frequency. 

        Parameters
        ----------
        numWindows : int
            The number of windows
        obs : np.ndarray
            The observations
        reg : np.ndarray
            The regressors

        Returns
        -------
        output : np.ndarray
            The solution to the regression problem
        varOutput : np.ndarray
            The variance
        """
        crossSize = len(self.crossChannels)
        # create array for output
        output = np.empty(shape=(self.outSize, self.inSize), dtype="complex")
        varOutput = np.empty(shape=(self.outSize, self.inSize), dtype="float")
        # solve
        for i in range(0, self.outSize):
            observation = obs[i, :]
            predictors = reg[i, :, :]
            # save the output
            out, resids, weights = chatterjeeMachler(
                predictors, observation, intercept=self.intercept
            )
            # out, resids, scale, weights = mmestimateModel(predictors, observation, intercept=self.intercept)

            # now take the weights, apply to the observations and predictors, stack the appropriate rows
            observation2 = np.zeros(shape=(crossSize), dtype="complex")
            predictors2 = np.zeros(shape=(crossSize, self.inSize), dtype="complex")
            for iChan in range(0, crossSize):
                # now need to have my indexing array
                indexArray = np.arange(iChan, numWindows * crossSize, crossSize)
                weightsLim = weights[indexArray]
                # weightsLim = weightsLim/np.sum(weightsLim) # normalise weights to 1
                observation2[iChan] = (
                    np.sum(obs[i, indexArray] * weightsLim) / numWindows
                )
                # now for the regressors
                for j in range(0, self.inSize):
                    predictors2[iChan, j] = (
                        np.sum(reg[i, indexArray, j] * weightsLim) / numWindows
                    )
            out, resids, weights = chatterjeeMachler(
                predictors2, observation2, intercept=self.intercept
            )
            # out, resids, scale, weights = mmestimateModel(
            #     predictors2, observation2, intercept=self.intercept)
            
            if self.intercept:
                out = out[1:]

            # now calculate out the varainces - have the solution out, have the weights
            # recalculate out the residuals with the final solution
            # calculate standard deviation of residuals
            # and then use chatterjee machler formula to estimate variances
            # this needs work - better to use an empirical bootstrap method, but this will do for now
            resids = np.absolute(observation - np.dot(predictors, out))
            scale = sampleMAD0(
                resids
            )  # some measure of standard deviation, rather than using the standard deviation
            residsVar = scale * scale
            # varPred = np.dot(hermitianTranspose(predictors), weights*predictors) # need to fix this
            varPred = np.dot(hermitianTranspose(predictors), predictors)
            varPred = np.linalg.inv(varPred)  # this is a pxp matrix
            varOut = 1.91472 * residsVar * varPred
            varOut = np.diag(varOut).real  # this should be a real number
            # if self.intercept:
            #     output[i] = out[1:]
            #     varOutput[i] = varOut[1:]
            # else:
            #     output[i] = out
            #     varOutput[i] = varOut
            output[i] = out
            varOutput[i] = varOut

        return output, varOutput

    def olsProcess(
        self, numWindows: int, obs: np.ndarray, reg: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Ordinary least squares regression processing

        Perform ordinary least regression processing using observations and regressors for a single evaluation frequency. 

        Parameters
        ----------
        numWindows : int
            The number of windows
        obs : np.ndarray
            The observations
        reg : np.ndarray
            The regressors

        Returns
        -------
        output : np.ndarray
            The solution to the regression problem
        varOutput : np.ndarray
            The variance        
        """
        # create array for output
        output = np.empty(shape=(self.outSize, self.inSize), dtype="complex")
        varOutput = np.empty(shape=(self.outSize, self.inSize), dtype="float")
        # solve
        for i in range(0, self.outSize):
            observation = obs[i, :]
            predictors = reg[i, :, :]
            # save the output
            out, resids, squareResid, rank, s = olsModel(
                predictors, observation, intercept=self.intercept
            )            
            if self.intercept:
                out = out[1:]

            # now calculate out the varainces - have the solution out, have the weights
            # recalculate out the residuals with the final solution
            # calculate standard deviation of residuals
            # and then use chatterjee machler formula to estimate variances
            # this needs work - better to use an empirical bootstrap method, but this will do for now
            resids = np.absolute(observation - np.dot(predictors, out))
            scale = sampleMAD0(
                resids
            )  # some measure of standard deviation, rather than using the standard deviation
            residsVar = scale * scale
            # varPred = np.dot(hermitianTranspose(predictors), weights*predictors) # need to fix this
            varPred = np.dot(hermitianTranspose(predictors), predictors)
            varPred = np.linalg.inv(varPred)  # this is a pxp matrix
            varOut = 1.91472 * residsVar * varPred
            varOut = np.diag(varOut).real  # this should be a real number
            # if self.intercept:
            #     output[i] = out[1:]
            #     varOutput[i] = varOut[1:]
            # else:
            #     output[i] = out
            #     varOutput[i] = varOut
            output[i] = out
            varOutput[i] = varOut            

        return output, varOutput

    def stackedProcess(self, data: np.ndarray) -> np.ndarray:
        """Ordinary least squares processing after stacking

        Parameters
        ----------
        data : np.ndarray
            Cross-spectra data

        Returns
        -------
        output : np.ndarray
            The solution to the regression problem
        varOutput : np.ndarray
            The variance        
        """
        # then do various sums
        numWindows = data.shape[0]
        crossSize = len(self.crossChannels)
        # unweighted sum (i.e. normal solution)
        unWeightedSum = np.sum(data, axis=0)
        unWeightedSum = unWeightedSum / numWindows

        # for each output variable, have ninput regressor variables
        # let's construct our arrays
        obs = np.empty(shape=(self.outSize, crossSize), dtype="complex")
        reg = np.empty(shape=(self.outSize, crossSize, self.inSize), dtype="complex")
        for i in range(0, self.outSize):
            for j, crossChan in enumerate(self.crossChannels):
                crossIndex = self.allChannels.index(crossChan)
                obs[i, j] = unWeightedSum[self.inSize + i, crossIndex]
                for k in range(0, self.inSize):
                    reg[i, j, k] = unWeightedSum[k, crossIndex]

        # create array for output
        output = np.empty(shape=(self.outSize, self.inSize), dtype="complex")

        for i in range(0, self.outSize):
            observation = obs[i, :]
            predictors = reg[i, :, :]
            # save the output
            out, resids, scale, weights = mmestimateModel(
                predictors, observation, intercept=self.intercept
            )
            if self.intercept:
                output[i] = out[1:]
            else:
                output[i] = out
        return output, output*0.1

    def writeTF(
        self,
        specdir: str,
        postpend: str,
        freq,
        data: np.ndarray,
        variances: np.ndarray,
        **kwargs
    ):
        """Write the transfer function file

        Parameters
        ----------
        specdir : str
            The spectra data being used for the transfer function estimate
        postpend : str
            The optional postpend to the transfer function file
        data : np.ndarray
            The transfer function estimates
        variances : np.ndarray
            The transfer function variances
        remotesite : str, optional
            Optionally, if there is a remote site
        remotechans : List[str], optional
            Optionally add the remote channels if there is a remote site
        """
        # path for writing out to
        sampleFreqStr = fileFormatSampleFreq(self.decParams.sampleFreq)
        if postpend == "":
            filename = "{}_fs{:s}_{}".format(self.outSite, sampleFreqStr, specdir)
        else:
            filename = "{}_fs{:s}_{}_{}".format(
                self.outSite, sampleFreqStr, specdir, postpend
            )
        datapath = os.path.join(self.outpath, sampleFreqStr)
        checkAndMakeDir(datapath)
        outfile = os.path.join(datapath, filename)
        # now construct the transferFunctionData object
        numFreq = len(freq)
        dataDict = {}
        varDict = {}
        for i in range(0, self.outSize):
            for j in range(0, self.inSize):
                key = "{}{}".format(self.outChannels[i], self.inChannels[j])
                dataArray = np.empty(shape=(numFreq), dtype="complex")
                varArray = np.empty(shape=(len(freq)), dtype="float")
                for ifreq in range(0, numFreq):
                    dataArray[ifreq] = data[ifreq][i, j]
                    varArray[ifreq] = variances[ifreq][i, j]
                dataDict[key] = dataArray
                varDict[key] = varArray
        tfData = TransferFunctionData(freq, dataDict, varDict)
        # now make the writer and write out
        tfWriter = TransferFunctionWriter(outfile, tfData)
        tfWriter.setHeaders(
            sampleFreq=self.decParams.sampleFreq,
            insite=self.inSite,
            inchans=self.inChannels,
            outsite=self.outSite,
            outchans=self.outChannels,
        )
        if "remotesite" in kwargs:
            tfWriter.addHeader("remotesite", kwargs["remotesite"])
        if "remotechans" in kwargs:
            tfWriter.addHeader("remotechans", kwargs["remotechans"])
        tfWriter.write()

    def printList(self) -> List[str]:
        """Class information as a list of strings

        Returns
        -------
        list
            List of strings with information
        """
        textLst = []
        textLst.append("In Site = {}".format(self.inSite))
        textLst.append("In Channels = {}".format(self.inChannels))
        textLst.append("Out Site = {}".format(self.outSite))
        textLst.append("Out Channels = {}".format(self.outChannels))
        textLst.append("Sample frequency = {:.3f}".format(self.decParams.sampleFreq))
        return textLst
