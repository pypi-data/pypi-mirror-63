import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from datetime import datetime
from typing import List, Union, Dict

from resistics.project.data import ProjectData
from resistics.site.data import SiteData
from resistics.time.data import TimeData
from resistics.spectra.io import SpectrumReader
from resistics.common.checks import parseKeywords, isMagnetic
from resistics.common.print import listToString, breakComment
from resistics.project.utils import projectText, projectWarning, projectError


def getSpecReader(
    projData: ProjectData, site: str, meas: str, **kwargs
) -> Union[SpectrumReader, None]:
    """Get the spectrum reader for a measurement

    Parameters
    ----------
    site : str
        Site for which to get the spectra reader
    meas : str
        The measurement
    options : Dict
        Options in a dictionary
    declevel : int, optional
        Decimation level for which to get data
    specdir : str, optional
        String that specifies spectra directory for the measurement

    Returns
    -------
    SpectrumReader
        The SpectrumReader object or None if data does not exist
    """
    options = {}
    options["declevel"]: int = 0
    options["specdir"]: str = projData.config.configParams["Spectra"]["specdir"]
    options = parseKeywords(options, kwargs)

    siteData = projData.getSiteData(site)
    measurements = siteData.getMeasurements()
    if meas not in measurements:
        projectError("Measurement directory {} not found".format(meas), quitRun=True)

    # create the spectrum reader
    specReader = SpectrumReader(
        os.path.join(siteData.getMeasurementSpecPath(meas), options["specdir"])
    )
    specReader.printInfo()

    # open the spectra file for the current decimation level if it exists
    check = specReader.openBinaryForReading("spectra", options["declevel"])
    if not check:
        projectWarning(
            "Spectra file does not exist at level {}".format(options["declevel"])
        )
        return None
    return specReader


def calculateSpectra(projData: ProjectData, **kwargs) -> None:
    """Calculate spectra for the project time data

    The philosophy is that spectra are calculated out for all data and later limited using statistics and time constraints

    Parameters
    ----------
    projData : ProjectData
        A project data object
    sites : str, List[str], optional
        Either a single site or a list of sites
    sampleFreqs : int, float, List[float], optional
        The frequencies in Hz for which to calculate the spectra. Either a single frequency or a list of them.
    chans : List[str], optional
        The channels for which to calculate out the spectra
    polreverse :  Dict[str, bool]
        Keys are channels and values are boolean flags for reversing
    scale : Dict[str, float]
        Keys are channels and values are floats to multiply the channel data by
    calibrate : bool, optional
        Flag whether to calibrate the data or not
    notch : List[float], optional
        List of frequencies to notch
    filter : Dict, optional
        Filter parameters
    specdir : str, optional
        The spectra directory to save the spectra data in
    ncores : int, optional
        The number of cores to run the transfer function calculations on        
    """
    from resistics.spectra.io import SpectrumWriter
    from resistics.decimate.decimator import Decimator
    from resistics.window.windower import Windower
    from resistics.project.shortcuts import (
        getCalibrator,
        getDecimationParameters,
        getWindowParameters,
    )
    from resistics.project.preprocess import (
        applyPolarisationReversalOptions,
        applyScaleOptions,
        applyCalibrationOptions,
        applyFilterOptions,
        applyNotchOptions,
    )

    options = {}
    options["sites"] = projData.getSites()
    options["sampleFreqs"]: List[float] = projData.getSampleFreqs()
    options["chans"]: List[str] = []
    options["polreverse"]: Union[bool, Dict[str, bool]] = False
    options["scale"]: Union[bool, Dict[str, float]] = False
    options["calibrate"]: bool = True
    options["notch"]: List[float] = []
    options["filter"]: Dict = {}
    options["specdir"]: str = projData.config.configParams["Spectra"]["specdir"]
    options["ncores"] = projData.config.getSpectraCores()
    options = parseKeywords(options, kwargs)

    # prepare calibrator
    cal = getCalibrator(projData.calPath, projData.config)
    if options["calibrate"]:
        cal.printInfo()

    datetimeRef = projData.refTime
    for site in options["sites"]:
        siteData = projData.getSiteData(site)
        siteData.printInfo()

        # calculate spectra for each frequency
        for sampleFreq in options["sampleFreqs"]:
            measurements = siteData.getMeasurements(sampleFreq)
            projectText(
                "Site {} has {:d} measurement(s) at sampling frequency {:.2f}".format(
                    site, len(measurements), sampleFreq
                )
            )
            if len(measurements) == 0:
                continue  # no data files at this sample rate

            for meas in measurements:
                projectText(
                    "Calculating spectra for site {} and measurement {}".format(
                        site, meas
                    )
                )
                # get measurement start and end times - this is the time of the first and last sample
                reader = siteData.getMeasurement(meas)
                startTime = siteData.getMeasurementStart(meas)
                stopTime = siteData.getMeasurementEnd(meas)
                dataChans = (
                    options["chans"]
                    if len(options["chans"]) > 0
                    else reader.getChannels()
                )
                timeData = reader.getPhysicalData(startTime, stopTime, chans=dataChans)
                timeData.addComment(breakComment())
                timeData.addComment("Calculating project spectra")
                timeData.addComment(projData.config.getConfigComment())
                # apply various options
                applyPolarisationReversalOptions(options, timeData)
                applyScaleOptions(options, timeData)
                applyCalibrationOptions(options, cal, timeData, reader)
                applyFilterOptions(options, timeData)
                applyNotchOptions(options, timeData)
                # define decimation and window parameters
                decParams = getDecimationParameters(sampleFreq, projData.config)
                numLevels = decParams.numLevels
                winParams = getWindowParameters(decParams, projData.config)
                dec = Decimator(timeData, decParams)
                timeData.addComment(
                    "Decimating with {} levels and {} frequencies per level".format(
                        numLevels, decParams.freqPerLevel
                    )
                )

                # loop through decimation levels
                for declevel in range(0, numLevels):
                    # get the data for the current level
                    check = dec.incrementLevel()
                    if not check:
                        break  # not enough data
                    timeData = dec.timeData

                    # create the windower and give it window parameters for current level
                    sampleFreqDec = dec.sampleFreq
                    win = Windower(
                        datetimeRef,
                        timeData,
                        winParams.getWindowSize(declevel),
                        winParams.getOverlap(declevel),
                    )
                    if win.numWindows < 2:
                        break  # do no more decimation

                    # print information and add some comments
                    projectText(
                        "Calculating spectra for decimation level {}".format(declevel)
                    )
                    timeData.addComment(
                        "Evaluation frequencies for this level {}".format(
                            listToString(decParams.getEvalFrequenciesForLevel(declevel))
                        )
                    )
                    timeData.addComment(
                        "Windowing with window size {} samples and overlap {} samples".format(
                            winParams.getWindowSize(declevel),
                            winParams.getOverlap(declevel),
                        )
                    )
                    if projData.config.configParams["Spectra"]["applywindow"]:
                        timeData.addComment(
                            "Performing fourier transform with window function {}".format(
                                projData.config.configParams["Spectra"]["windowfunc"]
                            )
                        )
                    else:
                        timeData.addComment(
                            "Performing fourier transform with no window function"
                        )

                    # collect time data
                    timeDataList = []
                    for iW in range(0, win.numWindows):
                        timeDataList.append(win.getData(iW))

                    # open spectra file for saving
                    specPath = os.path.join(
                        siteData.getMeasurementSpecPath(meas), options["specdir"]
                    )
                    specWrite = SpectrumWriter(specPath, datetimeRef)
                    specWrite.openBinaryForWriting(
                        "spectra",
                        declevel,
                        sampleFreqDec,
                        winParams.getWindowSize(declevel),
                        winParams.getOverlap(declevel),
                        win.winOffset,
                        win.numWindows,
                        dataChans,
                    )
                    if options["ncores"] > 0:
                        specDataList = multiSpectra(
                            options["ncores"],
                            timeDataList,
                            sampleFreqDec,
                            winParams.getWindowSize(declevel),
                            projData.config.configParams,
                        )
                    else:
                        specDataList = calculateWindowSpectra(
                            timeDataList,
                            sampleFreqDec,
                            winParams.getWindowSize(declevel),
                            projData.config.configParams,
                        )
                    # write out to spectra file
                    for iW in range(0, win.numWindows):
                        specWrite.writeBinary(specDataList[iW])
                    specWrite.writeCommentsFile(timeData.getComments())
                    specWrite.closeFile()


def calculateWindowSpectra(
    timeDataList: List[TimeData],
    sampleFreq: float,
    windowSize: int,
    config: Union[Dict, None] = None,
):
    """Calculate spectra for a list of TimeData

    Parameters
    ----------
    timeDataList : List[TimeData]
        A list of TimeData objects
    sampleFreq : float
        The sampling frequency of the TimeData
    windowSize : int
        The number of samples in the window
    
    Returns
    -------
    specDataList : List[SpectrumData]
        A list of spectra data
    """
    from resistics.spectra.calculator import SpectrumCalculator

    specCalc = SpectrumCalculator(sampleFreq, windowSize, config=config)
    numWindows = len(timeDataList)
    specDataList = list()
    # loop though windows and calculate spectra
    for iW in range(0, numWindows):
        timeData = timeDataList[iW]
        specDataList.append(specCalc.calcFourierCoeff(timeData))
    return specDataList


def multiSpectra(
    ncores: int,
    timeDataList: List[TimeData],
    sampleFreq: float,
    windowSize: int,
    config: Dict[str, None] = None,
):
    """Multiprocessing of spectra

    Parameters
    ----------
    ncores: int
        The number of cores for multiprocessing
    timeDataList : List[TimeData]
        A list of TimeData objects
    sampleFreq : float
        The sampling frequency of the TimeData
    windowSize : int
        The number of samples in the window
    
    Returns
    -------
    specDataList : List[SpectrumData]
        A list of spectra data    
    """
    import multiprocessing as mp

    # separate time data into batches
    numWindows = len(timeDataList)
    batchSize = int(np.ceil(numWindows / ncores))
    batches = []
    sizes = []
    for iB in range(0, ncores):
        batchStartWin = iB * batchSize
        if batchStartWin >= numWindows:
            break
        batchEndWin = batchStartWin + batchSize
        if batchEndWin > numWindows:
            batchEndWin = numWindows
        batch = []
        for iW in range(batchStartWin, batchEndWin):
            batch.append(timeDataList[iW])
        batches.append(batch)
        sizes.append(str(len(batch)))
    # set up tuples
    multiTuples = [(batch, sampleFreq, windowSize, config) for batch in batches]
    # multiprocess
    projectText("Running spectra calculations on {} cores".format(ncores))
    projectText(
        "{} windows being run in {} batches with sizes {}".format(
            numWindows, len(batches), ", ".join(sizes)
        )
    )
    with mp.Pool(ncores) as pool:
        out = pool.starmap(calculateWindowSpectra, multiTuples)
    # format the output into a single list
    specDataList = []
    for outBatch in out:
        specDataList = specDataList + outBatch
    return specDataList


def viewSpectra(
    projData: ProjectData, site: str, meas: str, **kwargs
) -> Union[Figure, None]:
    """View spectra for a measurement

    Parameters
    ----------
    projData : projecData
        The project data
    site : str
        The site to view
    meas: str
        The measurement of the site to view    
    chans : List[str], optional
        Channels to plot
    declevel : int, optional
        Decimation level to plot
    plotwindow : int, str, Dict, optional
        Windows to plot (local). If int, the window with local index plotwindow will be plotted. If string and "all", all the windows will be plotted if there are less than 20 windows, otherwise 20 windows throughout the whole spectra dataset will be plotted. If a dictionary, needs to have start and stop to define a range.
    specdir : str, optional
        String that specifies spectra directory for the measurement
    show : bool, optional
        Show the spectra plot
    save : bool, optional
        Save the plot to the images directory
    plotoptions : Dict, optional
        Dictionary of plot options
    
    Returns
    -------
    matplotlib.pyplot.figure or None
        A matplotlib figure unless the plot is not shown and is saved, in which case None and the figure is closed. If no data was found, then None is returned.
    """
    from resistics.common.plot import savePlot, plotOptionsSpec, colorbarMultiline

    options = {}
    options["chans"]: List[str] = []
    options["declevel"]: int = 0
    options["plotwindow"]: Union[int, Dict, str] = [0]
    options["specdir"]: str = projData.config.configParams["Spectra"]["specdir"]
    options["show"]: bool = True
    options["save"]: bool = False
    options["plotoptions"]: Dict = plotOptionsSpec()
    options = parseKeywords(options, kwargs)

    projectText("Plotting spectra for measurement {} and site {}".format(meas, site))
    specReader = getSpecReader(projData, site, meas, **options)
    if specReader is None:
        return None

    # channels
    dataChans = specReader.getChannels()
    if len(options["chans"]) > 0:
        dataChans = options["chans"]
    numChans = len(dataChans)

    # get windows
    numWindows = specReader.getNumWindows()
    sampleFreqDec = specReader.getSampleFreq()

    # get the window data
    windows = options["plotwindow"]
    if isinstance(windows, str) and windows == "all":
        if numWindows > 20:
            windows = list(
                np.linspace(0, numWindows, 20, endpoint=False, dtype=np.int32)
            )
        else:
            windows = list(np.arange(0, numWindows))
    elif isinstance(windows, int):
        windows = [windows]  # if an integer, make it into a list
    elif isinstance(windows, dict):
        windows = list(np.arange(windows["start"], windows["stop"] + 1))

    # create a figure
    plotfonts = options["plotoptions"]["plotfonts"]
    cmap = colorbarMultiline()
    fig = plt.figure(figsize=options["plotoptions"]["figsize"])
    for iW in windows:
        if iW >= numWindows:
            break
        color = cmap(iW / numWindows)
        winData = specReader.readBinaryWindowLocal(iW)
        winData.view(
            fig=fig,
            chans=dataChans,
            label="{} to {}".format(
                winData.startTime.strftime("%m-%d %H:%M:%S"),
                winData.stopTime.strftime("%m-%d %H:%M:%S"),
            ),
            plotfonts=plotfonts,
            color=color,
        )

    st = fig.suptitle(
        "Spectra plot, site = {}, meas = {}, fs = {:.2f} [Hz], decimation level = {:2d}".format(
            site, meas, sampleFreqDec, options["declevel"]
        ),
        fontsize=plotfonts["suptitle"],
    )
    st.set_y(0.98)

    # put on axis labels etc
    for idx, chan in enumerate(dataChans):
        ax = plt.subplot(numChans, 1, idx + 1)
        plt.title("Amplitude {}".format(chan), fontsize=plotfonts["title"])
        if len(options["plotoptions"]["amplim"]) == 2:
            ax.set_ylim(options["plotoptions"]["amplim"])
        ax.set_xlim(0, specReader.getSampleFreq() / 2.0)
        plt.grid(True)

    # fig legend and formatting
    ax = plt.gca()
    h, l = ax.get_legend_handles_labels()
    fig.tight_layout(rect=[0.02, 0.02, 0.77, 0.92])
    # legend axis
    legax = plt.axes(position=[0.77, 0.02, 0.23, 0.88], in_layout=False)
    plt.tick_params(left=False, labelleft=False, bottom=False, labelbottom="False")
    plt.box(False)
    legax.legend(h, l, loc="upper left", fontsize=plotfonts["legend"])

    # plot show and save
    if options["save"]:
        impath = projData.imagePath
        filename = "spectraData_{}_{}_dec{}_{}".format(
            site, meas, options["declevel"], options["specdir"]
        )
        savename = savePlot(impath, filename, fig)
        projectText("Image saved to file {}".format(savename))
    if options["show"]:
        plt.show(block=options["plotoptions"]["block"])
    if not options["show"] and options["save"]:
        plt.close(fig)
        return None
    return fig


def viewSpectraSection(
    projData: ProjectData, site: str, meas: str, **kwargs
) -> Union[Figure, None]:
    """View spectra section for a measurement

    Parameters
    ----------
    projData : projecData
        The project data
    site : str
        The site to view
    meas: str
        The measurement of the site to view    
    chans : List[str], optional
        Channels to plot
    declevel : int, optional
        Decimation level to plot
    specdir : str, optional
        String that specifies spectra directory for the measurement
    show : bool, optional
        Show the spectra plot
    save : bool, optional
        Save the plot to the images directory
    plotoptions : Dict, optional
        Dictionary of plot options
    
    Returns
    -------
    matplotlib.pyplot.figure or None
        A matplotlib figure unless the plot is not shown and is saved, in which case None and the figure is closed. If no data was found, then None is returned.
    """
    from matplotlib.colors import LogNorm

    from resistics.common.plot import savePlot, plotOptionsSpec, colorbar2dSpectra

    options = {}
    options["chans"] = []
    options["declevel"] = 0
    options["specdir"] = projData.config.configParams["Spectra"]["specdir"]
    options["show"] = True
    options["save"] = False
    options["plotoptions"] = plotOptionsSpec()
    options = parseKeywords(options, kwargs)

    projectText(
        "Plotting spectra section for measurement {} and site {}".format(meas, site)
    )
    specReader = getSpecReader(projData, site, meas, **options)
    if specReader is None:
        return None

    # channels
    dataChans = specReader.getChannels()
    if len(options["chans"]) > 0:
        dataChans = options["chans"]

    # get windows
    numWindows = specReader.getNumWindows()
    sampleFreqDec = specReader.getSampleFreq()
    f = specReader.getFrequencyArray()

    # if plotting a section, ignore plotwindow
    if numWindows > 250:
        windows = list(np.linspace(0, numWindows, 250, endpoint=False, dtype=np.int32))
    else:
        windows = np.arange(0, numWindows)

    # create figure
    plotfonts = options["plotoptions"]["plotfonts"]
    fig = plt.figure(figsize=options["plotoptions"]["figsize"])
    st = fig.suptitle(
        "Spectra section, site = {}, meas = {}, fs = {:.2f} [Hz], decimation level = {:2d}, windows = {:d}, {} to {}".format(
            site,
            meas,
            sampleFreqDec,
            options["declevel"],
            len(windows),
            windows[0],
            windows[-1],
        ),
        fontsize=plotfonts["suptitle"],
    )
    st.set_y(0.98)

    # collect the data
    specData = np.empty(
        shape=(len(windows), len(dataChans), specReader.getDataSize()), dtype="complex"
    )
    dates = []
    for idx, iW in enumerate(windows):
        winData = specReader.readBinaryWindowLocal(iW)
        for cIdx, chan in enumerate(dataChans):
            specData[idx, cIdx, :] = winData.data[chan]
        dates.append(winData.startTime)

    ampLim = options["plotoptions"]["amplim"]
    for idx, chan in enumerate(dataChans):
        ax = plt.subplot(1, len(dataChans), idx + 1)
        plotData = np.transpose(np.absolute(np.squeeze(specData[:, idx, :])))
        if len(ampLim) == 2:
            plt.pcolor(
                dates,
                f,
                plotData,
                norm=LogNorm(vmin=ampLim[0], vmax=ampLim[1]),
                cmap=colorbar2dSpectra(),
            )
        else:
            plt.pcolor(
                dates,
                f,
                plotData,
                norm=LogNorm(vmin=plotData.min(), vmax=plotData.max()),
                cmap=colorbar2dSpectra(),
            )
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=plotfonts["axisTicks"])
        # set axis limits
        ax.set_ylim(0, specReader.getSampleFreq() / 2.0)
        ax.set_xlim([dates[0], dates[-1]])
        if isMagnetic(chan):
            plt.title("Amplitude {} [nT]".format(chan), fontsize=plotfonts["title"])
        else:
            plt.title("Amplitude {} [mV/km]".format(chan), fontsize=plotfonts["title"])
        ax.set_ylabel("Frequency [Hz]", fontsize=plotfonts["axisLabel"])
        ax.set_xlabel("Time", fontsize=plotfonts["axisLabel"])
        # set tick sizes
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(plotfonts["axisTicks"])
        plt.grid(True)

    # plot format
    fig.autofmt_xdate(rotation=90, ha="center")
    fig.tight_layout(rect=[0.02, 0.02, 0.96, 0.92])

    # plot show and save
    if options["save"]:
        impath = projData.imagePath
        filename = "spectraSection_{}_{}_dec{}_{}".format(
            site, meas, options["declevel"], options["specdir"]
        )
        savename = savePlot(impath, filename, fig)
        projectText("Image saved to file {}".format(savename))
    if options["show"]:
        plt.show(block=options["plotoptions"]["block"])
    if not options["show"] and options["save"]:
        plt.close(fig)
        return None
    return fig


def viewSpectraStack(
    projData: ProjectData, site: str, meas: str, **kwargs
) -> Union[Figure, None]:
    """View spectra stacks for a measurement

    Parameters
    ----------
    projData : projecData
        The project data
    site : str
        The site to view
    meas: str
        The measurement of the site to view
    chans : List[str], optional
        Channels to plot
    declevel : int, optional
        Decimation level to plot
    numstacks : int, optional
        The number of windows to stack
    coherences : List[List[str]], optional
        A list of coherences to add, specified as [["Ex", "Hy"], ["Ey", "Hx"]] 
    specdir : str, optional
        String that specifies spectra directory for the measurement
    show : bool, optional
        Show the spectra plot
    save : bool, optional
        Save the plot to the images directory
    plotoptions : Dict, optional
        Dictionary of plot options
    
    Returns
    -------
    matplotlib.pyplot.figure or None
        A matplotlib figure unless the plot is not shown and is saved, in which case None and the figure is closed. If no data was found, then None is returned.
    """
    from resistics.common.plot import savePlot, plotOptionsSpec, colorbarMultiline

    options = {}
    options["chans"] = []
    options["declevel"] = 0
    options["numstacks"] = 10
    options["coherences"] = []
    options["specdir"] = projData.config.configParams["Spectra"]["specdir"]
    options["show"] = True
    options["save"] = False
    options["plotoptions"] = plotOptionsSpec()
    options = parseKeywords(options, kwargs)

    projectText(
        "Plotting spectra stack for measurement {} and site {}".format(meas, site)
    )
    specReader = getSpecReader(projData, site, meas, **options)
    if specReader is None:
        return None

    # channels
    dataChans = specReader.getChannels()
    if len(options["chans"]) > 0:
        dataChans = options["chans"]
    numChans = len(dataChans)

    # get windows
    numWindows = specReader.getNumWindows()
    sampleFreqDec = specReader.getSampleFreq()
    f = specReader.getFrequencyArray()

    # calculate num of windows to stack in each set
    stackSize = int(np.floor(1.0 * numWindows / options["numstacks"]))
    if stackSize == 0:
        projectWarning(
            "Too few windows for number of stacks {}".format(options["numstacks"])
        )
        options["numstacks"] = numWindows
        stackSize = 1
        projectWarning("Number of stacks changed to {}".format(options["numstacks"]))

    # calculate number of rows - in case interested in coherences too
    nrows = (
        2
        if len(options["coherences"]) == 0
        else 2 + np.ceil(1.0 * len(options["coherences"]) / numChans)
    )

    # setup the figure
    plotfonts = options["plotoptions"]["plotfonts"]
    cmap = colorbarMultiline()
    fig = plt.figure(figsize=options["plotoptions"]["figsize"])
    st = fig.suptitle(
        "Spectra stack, fs = {:.6f} [Hz], decimation level = {:2d}, windows in each set = {:d}".format(
            sampleFreqDec, options["declevel"], stackSize
        ),
        fontsize=plotfonts["suptitle"],
    )
    st.set_y(0.98)

    # do the stacking
    for iP in range(0, options["numstacks"]):
        stackStart = iP * stackSize
        stackStop = min(stackStart + stackSize, numWindows)
        color = cmap(iP / options["numstacks"])
        # dictionaries to hold data for this section
        stackedData = {}
        ampData = {}
        phaseData = {}
        powerData = {}

        # assign initial zeros
        for c in dataChans:
            stackedData[c] = np.zeros(shape=(specReader.getDataSize()), dtype="complex")
            ampData[c] = np.zeros(shape=(specReader.getDataSize()), dtype="complex")
            phaseData[c] = np.zeros(shape=(specReader.getDataSize()), dtype="complex")
            for c2 in dataChans:
                powerData[c + c2] = np.zeros(
                    shape=(specReader.getDataSize()), dtype="complex"
                )

        # now stack the data and create nice plots
        for iW in range(stackStart, stackStop):
            winData = specReader.readBinaryWindowLocal(iW)
            for c in dataChans:
                stackedData[c] += winData.data[c]
                ampData[c] += np.absolute(winData.data[c])
                phaseData[c] += np.angle(winData.data[c]) * (180.0 / np.pi)
                # get coherency data
                for c2 in dataChans:
                    powerData[c + c2] += winData.data[c] * np.conjugate(
                        winData.data[c2]
                    )
            if iW == stackStart:
                startTime = winData.startTime
            if iW == stackStop - 1:
                stopTime = winData.stopTime

        # scale powers and stacks
        ampLim = options["plotoptions"]["amplim"]
        for idx, c in enumerate(dataChans):
            stackedData[c] = stackedData[c] / (stackStop - stackStart)
            ampData[c] = ampData[c] / (stackStop - stackStart)
            phaseData[c] = phaseData[c] / (stackStop - stackStart)
            for c2 in dataChans:
                # normalisation
                powerData[c + c2] = 2 * powerData[c + c2] / (stackStop - stackStart)
                # normalisation
                powerData[c + c2][[0, -1]] = powerData[c + c2][[0, -1]] / 2

            # plot
            ax1 = plt.subplot(nrows, numChans, idx + 1)
            plt.title("Amplitude {}".format(c), fontsize=plotfonts["title"])
            h = ax1.semilogy(
                f,
                ampData[c],
                color=color,
                label="{} to {}".format(
                    startTime.strftime("%m-%d %H:%M:%S"),
                    stopTime.strftime("%m-%d %H:%M:%S"),
                ),
            )
            if len(ampLim) == 2:
                ax1.set_ylim(ampLim)
            else:
                ax1.set_ylim(0.01, 1000)
            ax1.set_xlim(0, sampleFreqDec / 2.0)
            if isMagnetic(c):
                ax1.set_ylabel("Amplitude [nT]", fontsize=plotfonts["axisLabel"])
            else:
                ax1.set_ylabel("Amplitude [mV/km]", fontsize=plotfonts["axisLabel"])
            ax1.set_xlabel("Frequency [Hz]", fontsize=plotfonts["axisLabel"])
            plt.grid(True)

            # set tick sizes
            for label in ax1.get_xticklabels() + ax1.get_yticklabels():
                label.set_fontsize(plotfonts["axisTicks"])
            # plot phase
            ax2 = plt.subplot(nrows, numChans, numChans + idx + 1)
            plt.title("Phase {}".format(c), fontsize=plotfonts["title"])
            ax2.plot(
                f,
                phaseData[c],
                color=color,
                label="{} to {}".format(
                    startTime.strftime("%m-%d %H:%M:%S"),
                    stopTime.strftime("%m-%d %H:%M:%S"),
                ),
            )
            ax2.set_ylim(-180, 180)
            ax2.set_xlim(0, sampleFreqDec / 2.0)
            ax2.set_ylabel("Phase [degrees]", fontsize=plotfonts["axisLabel"])
            ax2.set_xlabel("Frequency [Hz]", fontsize=plotfonts["axisLabel"])
            plt.grid(True)
            # set tick sizes
            for label in ax2.get_xticklabels() + ax2.get_yticklabels():
                label.set_fontsize(plotfonts["axisTicks"])

        # plot coherences
        for idx, coh in enumerate(options["coherences"]):
            c = coh[0]
            c2 = coh[1]
            cohNom = np.power(np.absolute(powerData[c + c2]), 2)
            cohDenom = powerData[c + c] * powerData[c2 + c2]
            coherence = cohNom / cohDenom
            ax = plt.subplot(nrows, numChans, 2 * numChans + idx + 1)
            plt.title("Coherence {} - {}".format(c, c2), fontsize=plotfonts["title"])
            ax.plot(
                f,
                coherence,
                color=color,
                label="{} to {}".format(
                    startTime.strftime("%m-%d %H:%M:%S"),
                    stopTime.strftime("%m-%d %H:%M:%S"),
                ),
            )
            ax.set_ylim(0, 1.1)
            ax.set_xlim(0, sampleFreqDec / 2)
            ax.set_ylabel("Coherence", fontsize=plotfonts["axisLabel"])
            ax.set_xlabel("Frequency [Hz]", fontsize=plotfonts["axisLabel"])
            plt.grid(True)
            # set tick sizes
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(plotfonts["axisTicks"])

    # fig legend and layout
    ax = plt.gca()
    h, l = ax.get_legend_handles_labels()
    fig.tight_layout(rect=[0.01, 0.01, 0.98, 0.81])
    # legend
    legax = plt.axes(position=[0.01, 0.82, 0.98, 0.12], in_layout=False)
    plt.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    plt.box(False)
    legax.legend(h, l, ncol=4, loc="upper center", fontsize=plotfonts["legend"])

    # plot show and save
    if options["save"]:
        impath = projData.imagePath
        filename = "spectraStack_{}_{}_dec{}_{}".format(
            site, meas, options["declevel"], options["specdir"]
        )
        savename = savePlot(impath, filename, fig)
        projectText("Image saved to file {}".format(savename))
    if options["show"]:
        plt.show(block=options["plotoptions"]["block"])
    if not options["show"] and options["save"]:
        plt.close(fig)
        return None
    return fig
