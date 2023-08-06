import sys
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Union, List, Dict

from resistics.common.checks import parseKeywords, isElectric, isMagnetic
from resistics.common.io import checkFilepath, fileFormatSampleFreq
from resistics.common.print import arrayToString
from resistics.project.data import ProjectData
from resistics.project.utils import projectText, projectWarning, projectError
from resistics.site.data import SiteData
from resistics.transfunc.data import TransferFunctionData


def getTransferFunctionData(
    projData: ProjectData, site: str, sampleFreq: float, **kwargs
) -> TransferFunctionData:
    """Get transfer function data

    Parameters
    ----------
    projData : projecData
        The project data
    site : str
        Site to get the transfer functiond data for
    sampleFreq : int, float
        The sampling frequency for which to get the transfer function data
    specdir : str, optional
        The spectra directories used
    postpend : str, optional
        The postpend on the transfer function files
    """
    from resistics.transfunc.io import TransferFunctionReader

    options: Dict = dict()
    options["specdir"]: str = projData.config.configParams["Spectra"]["specdir"]
    options["postpend"]: str = ""
    options = parseKeywords(options, kwargs)

    # deal with the postpend
    if options["postpend"] != "":
        postpend = "_{}".format(options["postpend"])
    else:
        postpend = options["postpend"]

    siteData = projData.getSiteData(site)
    sampleFreqStr = fileFormatSampleFreq(sampleFreq)
    path = os.path.join(
        siteData.transFuncPath,
        "{:s}".format(sampleFreqStr),
        "{}_fs{:s}_{}{}".format(site, sampleFreqStr, options["specdir"], postpend),
    )
    # check path
    if not checkFilepath(path):
        projectWarning("No transfer function file with name {}".format(path))
        return False

    projectText(
        "Reading transfer function for site {}, sample frequency {}, file {}".format(
            site, sampleFreq, path
        )
    )

    tfReader = TransferFunctionReader(path)
    tfReader.printInfo()
    return tfReader.tfData


def processProject(projData: ProjectData, **kwargs) -> None:
    """Process a project

    Parameters
    ----------
    projData : ProjectData
        The project data instance for the project    
    sites : List[str], optional
        List of sites 
    sampleFreqs : List[float], optional
        List of sample frequencies to process
    specdir : str, optional
        The spectra directories to use
    inchans : List[str], optional
        Channels to use as the input of the linear system
    inputsite : str, optional
        Site from which to take the input channels. The default is to use input and output channels from the same site        
    outchans : List[str], optional
        Channels to use as the output of the linear system
    remotesite : str, optional
        The site to use as the remote site
    remotechans : List[str], optional
        Channels to use from the remote reference site
    crosschannels : List[str], optional
        List of channels to use for cross powers
    masks : Dict, optional
        Masks dictionary for passing mask data. The key should be a site name and the value should either be a string for a single mask or a list of multiple masks.
    datetimes : List, optional
        List of datetime constraints, each one as a dictionary. For example [{"type": "datetime", "start": 2018-08-08 00:00:00, "end": 2018-08-08 16:00:00, "levels": [0,1]}]. Note that levels is optional.            
    postpend : str, optional
        String to postpend to the transfer function output
    ncores : int, optional
        The number of cores to run the transfer function calculations on        
    """
    options: Dict = dict()
    options["sites"]: List[str] = projData.getSites()
    options["sampleFreqs"]: List[float] = projData.getSampleFreqs()
    options["specdir"]: str = projData.config.configParams["Spectra"]["specdir"]
    options["inchans"]: List[str] = ["Hx", "Hy"]
    options["inputsite"]: str = ""
    options["outchans"]: List[str] = ["Ex", "Ey"]
    options["remotesite"]: str = ""
    options["remotechans"]: List[str] = options["inchans"]
    options["crosschannels"]: List[str] = []
    options["masks"]: Dict = {}
    options["datetimes"]: List = []
    options["postpend"]: str = ""
    options["ncores"] = projData.config.getSolverCores()    
    options = parseKeywords(options, kwargs)

    for site in options["sites"]:
        siteData = projData.getSiteData(site)
        siteFreqs = siteData.getSampleFreqs()
        for sampleFreq in siteFreqs:
            # check if not included
            if sampleFreq not in options["sampleFreqs"]:
                continue
            processSite(projData, site, sampleFreq, **options)


def processSite(
    projData: ProjectData, site: str, sampleFreq: Union[int, float], **kwargs
):
    """Process a single sampling frequency for a site

    The site passed is assumed to be the output site (the output channels will come from this site). If channels from a different site are desired to be used as the input channels, this can be done by specifying the optional inputsite argument.

    .. todo:: 
    
        Give a few different examples here

    Parameters
    ----------
    projData : ProjectData
        The project data instance for the project
    site : str
        Site to process 
    sampleFreq : float, int
        Sample frequency to process
    specdir : str, optional
        The spectra directories to use
    inchans : List[str], optional
        Channels to use as the input of the linear system
    inputsite : str, optional
        Site from which to take the input channels. The default is to use input and output channels from the same site
    outchans : List[str], optional
        Channels to use as the output of the linear system
    remotesite : str, optional
        The site to use as the remote site
    remotechans : List[str], optional
        Channels to use from the remote reference site
    crosschannels : List[str], optional
        List of channels to use for cross powers
    masks : Dict, optional
        Masks dictionary for passing mask data. The key should be a site name and the value should either be a string for a single mask or a list of multiple masks.
    datetimes : List, optional
        List of datetime constraints, each one as a dictionary. For example [{"type": "datetime", "start": 2018-08-08 00:00:00, "end": 2018-08-08 16:00:00, "levels": [0,1]}]. Note that levels is optional.
    postpend : str, optional
        String to postpend to the transfer function output
    ncores : int, optional
        The number of cores to run the transfer function calculations on
    """
    from resistics.decimate.decimator import Decimator
    from resistics.window.selector import WindowSelector
    from resistics.project.shortcuts import (
        getDecimationParameters,
        getWindowParameters,
        getWindowSelector,
        getLocalRegressor,
        getRemoteRegressor,
    )

    options = {}
    options["specdir"] = projData.config.configParams["Spectra"]["specdir"]
    options["inchans"] = ["Hx", "Hy"]
    options["inputsite"] = ""
    options["outchans"] = ["Ex", "Ey"]
    options["remotesite"] = ""
    options["remotechans"] = options["inchans"]
    options["crosschannels"] = []
    options["masks"] = {}
    options["datetimes"] = []
    options["postpend"] = ""
    options["ncores"] = projData.config.getSolverCores()
    options = parseKeywords(options, kwargs)
    if options["inputsite"] == "":
        options["inputsite"] = site

    projectText("Processing site {}, sampling frequency {}".format(site, sampleFreq))
    siteData = projData.getSiteData(site)

    # define decimation parameters
    decParams = getDecimationParameters(sampleFreq, projData.config)
    decParams.printInfo()
    winParams = getWindowParameters(decParams, projData.config)
    # window selector
    winSelector = getWindowSelector(projData, decParams, winParams, options["specdir"])

    # if two sites are duplicated (e.g. input site and output site), winSelector only uses distinct sites. Hence using site and inputSite is no problem even if they are the same
    processSites = []
    if options["remotesite"]:
        processSites = [site, options["inputsite"], options["remotesite"]]
        winSelector.setSites(processSites)
    else:
        # if no remote site, then single site processing
        processSites = [site, options["inputsite"]]
        winSelector.setSites(processSites)

    # add window masks
    if len(list(options["masks"].keys())) > 0:
        for maskSite in options["masks"]:
            if maskSite not in processSites:
                # there is a site in the masks dictionary which is of no interest
                continue
            if isinstance(options["masks"][maskSite], str):
                # a single mask
                winSelector.addWindowMask(maskSite, options["masks"][maskSite])
                continue
            if all(isinstance(item, str) for item in options["masks"][maskSite]):
                # list of masks for the site
                for mask in options["masks"][maskSite]:
                    winSelector.addWindowMask(maskSite, mask)

    # add datetime constraints
    for dC in options["datetimes"]:
        levels = None
        if "levels" in dC:
            levels = dC["levels"]

        if dC["type"] == "datetime":
            winSelector.addDatetimeConstraint(dC["start"], dC["stop"], levels)
        if dC["type"] == "time":
            winSelector.addTimeConstraint(dC["start"], dC["stop"], levels)
        if dC["type"] == "date":
            winSelector.addDateConstraint(dC["date"], levels)

    # calculate the shared windows and print info
    winSelector.calcSharedWindows()
    winSelector.printInfo()
    winSelector.printDatetimeConstraints()
    winSelector.printWindowMasks()
    winSelector.printSharedWindows()
    winSelector.printWindowsForFrequency()

    # now have the windows, pass the winSelector to processors
    outPath = siteData.transFuncPath
    if options["remotesite"]:
        projectText(
            "Remote reference processing with sites: in = {}, out = {}, reference = {}".format(
                options["inputsite"], site, options["remotesite"]
            )
        )
        processor = getRemoteRegressor(winSelector, outPath, projData.config)
        processor.setRemote(options["remotesite"], options["remotechans"])
    else:
        projectText(
            "Single site processing with sites: in = {}, out = {}".format(
                options["inputsite"], site
            )
        )
        processor = getLocalRegressor(winSelector, outPath, projData.config)

    # add the input and output site
    processor.setInput(options["inputsite"], options["inchans"])
    processor.setOutput(site, options["outchans"])
    if len(options["crosschannels"]) > 0:
        processor.crossChannels = options["crosschannels"]
    processor.postpend = options["postpend"]
    processor.printInfo()
    projectText("Processing data using {} cores".format(options["ncores"]))
    processor.process(options["ncores"])


def viewImpedance(projData: ProjectData, **kwargs) -> List[Figure]:
    """View impedance tensor data

    Parameters
    ----------
    projData : projecData
        The project data
    sites : List[str], optional
        List of sites to plot transfer functions for
    sampleFreqs : List[float], optional 
        List of samples frequencies for which to plot transfer functions
    polarisations : List[str], optional 
        A list of polarisations to plot. For example, ["ExHx", "ExHy", "EyHx", "EyHy"]
    specdir : str, optional
        The spectra directories used
    postpend : str, optional
        The postpend on the transfer function files
    oneplot : bool, optional
        Plot the polarisation on a single plot
    show : bool, optional
        Show the spectra plot
    save : bool, optional
        Save the plot to the images directory
    plotoptions : Dict
        A dictionary of plot options. For example, set the resistivity y limits using res_ylim, set the phase y limits using phase_ylim and set the xlimits using xlim
    """
    from resistics.common.plot import (
        savePlot,
        plotOptionsTransferFunction,
        getTransferFunctionFigSize,
        transferFunctionColours,
    )

    options = {}
    options["sites"] = projData.getSites()
    options["sampleFreqs"] = projData.getSampleFreqs()
    options["polarisations"] = ["ExHx", "ExHy", "EyHx", "EyHy"]
    options["specdir"] = projData.config.configParams["Spectra"]["specdir"]
    options["postpend"] = ""
    options["oneplot"] = True
    options["save"] = False
    options["show"] = True
    options["plotoptions"] = plotOptionsTransferFunction()
    options = parseKeywords(options, kwargs)

    # loop over sites
    figs = []
    for site in options["sites"]:
        siteData = projData.getSiteData(site)
        sampleFreqs = set(siteData.getSampleFreqs())
        # find the intersection with the options["freqs"]
        sampleFreqs = sampleFreqs.intersection(options["sampleFreqs"])
        sampleFreqs = sorted(list(sampleFreqs))

        # if prepend is a string, then make it a list
        if isinstance(options["postpend"], str):
            options["postpend"] = [options["postpend"]]

        plotfonts = options["plotoptions"]["plotfonts"]
        # now loop over the postpend options
        for pp in options["postpend"]:
            # add an underscore if not empty
            postpend = "_{}".format(pp) if pp != "" else pp

            if options["plotoptions"]["figsize"] is None:
                figsize = getTransferFunctionFigSize(
                    options["oneplot"], len(options["polarisations"])
                )
            else:
                figsize = options["plotoptions"]["figsize"]
            fig = plt.figure(figsize=figsize)
            mks = ["o", "*", "d", "^", "h"]
            lstyles = ["solid", "dashed", "dashdot", "dotted"]
            colours = transferFunctionColours()

            # loop over sampling frequencies
            includedFreqs = []
            for idx, sampleFreq in enumerate(sampleFreqs):

                tfData = getTransferFunctionData(
                    projData, site, sampleFreq, specdir=options["specdir"], postpend=pp
                )
                if not tfData:
                    continue

                includedFreqs.append(sampleFreq)
                projectText(
                    "Plotting transfer function for site {}, sample frequency {}".format(
                        site, sampleFreq
                    )
                )

                # plot
                mk = mks[idx % len(mks)]
                ls = lstyles[idx % len(lstyles)]
                tfData.viewImpedance(
                    fig=fig,
                    polarisations=options["polarisations"],
                    mk=mk,
                    ls=ls,
                    colours=colours,
                    oneplot=options["oneplot"],
                    res_ylim=options["plotoptions"]["res_ylim"],
                    phase_ylim=options["plotoptions"]["phase_ylim"],
                    xlim=options["plotoptions"]["xlim"],
                    label="{}".format(sampleFreq),
                    plotfonts=options["plotoptions"]["plotfonts"],
                )

            # check if any files found
            if len(includedFreqs) == 0:
                continue

            # sup title
            sub = "Site {}: {}".format(site, options["specdir"] + postpend)
            sub = "{}\nfs = {}".format(sub, arrayToString(includedFreqs, decimals=3))
            st = fig.suptitle(sub, fontsize=plotfonts["suptitle"])
            st.set_y(0.99)
            fig.tight_layout()
            fig.subplots_adjust(top=0.92)
            figs.append(fig)

            if options["save"]:
                impath = projData.imagePath
                filename = "transFunction_{}_{}{}".format(
                    site, options["specdir"], postpend
                )
                savename = savePlot(impath, filename, fig)
                projectText("Image saved to file {}".format(savename))

        if not options["show"]:
            plt.close("all")
        else:
            plt.show(block=options["plotoptions"]["block"])

    return figs


def viewTipper(projData: ProjectData, **kwargs) -> List[Figure]:
    """View transfer function data

    Parameters
    ----------
    projData : projecData
        The project data
    sites : List[str], optional
        List of sites to plot transfer functions for
    sampleFreqs : List[float], optional 
        List of samples frequencies for which to plot transfer functions
    specdir : str, optional
        The spectra directories used
    postpend : str, optional
        The postpend on the transfer function files
    cols : bool, optional
        Boolean flag, True to arrange tipper plot as 1 row with 3 columns
    show : bool, optional
        Show the spectra plot
    save : bool, optional
        Save the plot to the images directory
    plotoptions : Dict
        A dictionary of plot options. For example, set the resistivity y limits using res_ylim, set the phase y limits using phase_ylim and set the xlimits using xlim
    """
    from resistics.common.plot import (
        savePlot,
        plotOptionsTipper,
        getTransferFunctionFigSize,
        transferFunctionColours,
    )

    options = {}
    options["sites"] = projData.getSites()
    options["sampleFreqs"] = projData.getSampleFreqs()
    options["specdir"] = projData.config.configParams["Spectra"]["specdir"]
    options["postpend"] = ""
    options["cols"] = True
    options["save"] = False
    options["show"] = True
    options["plotoptions"] = plotOptionsTipper()
    options = parseKeywords(options, kwargs)

    # loop over sites
    figs = []
    for site in options["sites"]:
        siteData = projData.getSiteData(site)
        sampleFreqs = set(siteData.getSampleFreqs())
        # find the intersection with the options["freqs"]
        sampleFreqs = sampleFreqs.intersection(options["sampleFreqs"])
        sampleFreqs = sorted(list(sampleFreqs))

        # if prepend is a string, then make it a list
        if isinstance(options["postpend"], str):
            options["postpend"] = [options["postpend"]]

        plotfonts = options["plotoptions"]["plotfonts"]
        # now loop over the postpend options
        for pp in options["postpend"]:
            # add an underscore if not empty
            postpend = "_{}".format(pp) if pp != "" else pp

            fig = plt.figure(figsize=options["plotoptions"]["figsize"])
            mks = ["o", "*", "d", "^", "h"]
            lstyles = ["solid", "dashed", "dashdot", "dotted"]

            # loop over sampling frequencies
            includedFreqs = []
            for idx, sampleFreq in enumerate(sampleFreqs):

                tfData = getTransferFunctionData(
                    projData, site, sampleFreq, specdir=options["specdir"], postpend=pp
                )
                if not tfData:
                    continue

                includedFreqs.append(sampleFreq)
                projectText(
                    "Plotting tipper for site {}, sample frequency {}".format(
                        site, sampleFreq
                    )
                )

                mk = mks[idx % len(mks)]
                ls = lstyles[idx % len(lstyles)]
                tfData.viewTipper(
                    fig=fig,
                    rows=options["cols"],
                    mk=mk,
                    ls=ls,
                    label="{}".format(sampleFreq),
                    xlim=options["plotoptions"]["xlim"],
                    length_ylim=options["plotoptions"]["length_ylim"],
                    angle_ylim=options["plotoptions"]["angle_ylim"],
                    plotfonts=options["plotoptions"]["plotfonts"],
                )

            # check if any files found
            if len(includedFreqs) == 0:
                continue

            # sup title
            sub = "Site {} tipper: {}".format(site, options["specdir"] + postpend)
            sub = "{}\nfs = {}".format(sub, arrayToString(includedFreqs, decimals=3))
            st = fig.suptitle(sub, fontsize=plotfonts["suptitle"])
            st.set_y(0.99)
            fig.tight_layout()
            fig.subplots_adjust(top=0.85)
            figs.append(fig)

            if options["save"]:
                impath = projData.imagePath
                filename = "tipper_{}_{}{}".format(site, options["specdir"], postpend)
                savename = savePlot(impath, filename, fig)
                projectText("Image saved to file {}".format(savename))

        if not options["show"]:
            plt.close("all")
        else:
            plt.show(block=options["plotoptions"]["block"])
    return figs
