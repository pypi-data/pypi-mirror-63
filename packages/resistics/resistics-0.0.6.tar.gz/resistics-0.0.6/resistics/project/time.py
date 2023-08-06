import sys
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, Union, List

from resistics.project.data import ProjectData
from resistics.time.reader import TimeReader
from resistics.time.writer_internal import TimeWriterInternal
from resistics.common.checks import parseKeywords, isElectric
from resistics.project.utils import projectText, projectBlock, checkDateOptions


def getTimeReader(projData: ProjectData, site: str, meas: str) -> TimeReader:
    """Get a data reader object for a measurement

    Data readers will then return a timeData object when given a sample range of data to return for

    Parameters
    ----------
    projData : ProjectData
        A project data object
    site : str
        The site for which to get the data reader
    meas : str
        The measurement in the site for which to get the data reader

    Returns
    -------
    DataReader
        A data reader object which allows a user to get time data
    """
    siteData = projData.getSiteData(site)
    return siteData.getMeasurement(meas)


def preProcess(projData: ProjectData, **kwargs) -> None:
    """Pre-process project time data

    Preprocess the time data using filters, notch filters, resampling or interpolation. A new measurement folder is created under the site. The name of the new measurement folder is:
    prepend_[name of input measurement]_postpend. By default, prepend is "proc" and postpend is empty. 

    Processed time series data can be saved in a new site by using the outputsite option.

    Parameters
    ----------
    projData : ProjectData
        A project data object
    sites : str, List[str], optional
        Either a single site or a list of sites
    sampleFreqs : int, float, List[float], optional
        The frequencies to preprocess
    start : str, optional
        Start date of data to preprocess in format "%Y-%m-%d %H:%M:%S"
    stop : str, optional
        Stop date of data to process in format "%Y-%m-%d %H:%M:%S"
    outputsite : str, optional
        A site to output the preprocessed time data to. If this site does not exist, it will be created
    polreverse :  Dict[str, bool]
        Keys are channels and values are boolean flags for reversing 
    scale : Dict[str, float]
        Keys are channels and values are floats to multiply the channel data by   
    calibrate : bool, optional
        Boolean flag for calibrating the data. Default is false and setting to True will calibrate where files can be found.
    normalise : bool, optional
        Boolean flag for normalising the data. Default is False and setting to True will normalise each channel independently.
    filter : Dict, optional
        Filtering options in a dictionary
    notch : List[float], optional
        List of frequencies to notch in spectra given as a list of floats
    resamp : Dict, optional
        Resampling parameters in a dictionary with entries in the format: {sampleRateFrom: sampleRateTo}. All measurement directories of sampleRateFrom will be resampled to sampleRateTo
    interp : bool, optional
        Boolean flag for interpolating the data on to the second, so that sampling is coincident with seconds. This is not always the case. For example, SPAM data is not necessarily sampled on the second, whereas ATS data is. This function is useful when combining data of multiple formats. Interpolation does not change the sampling rate. Default is False.
    prepend : str, optional
        String to prepend to the output folder. Default is "proc".
    postpend : str, optional
        String to postpend to the output folder. Default is empty.
    """
    from resistics.project.shortcuts import getCalibrator
    from resistics.project.preprocess import (
        applyPolarisationReversalOptions,
        applyScaleOptions,
        applyCalibrationOptions,
        applyFilterOptions,
        applyInterpolationOptions,
        applyNormaliseOptions,
        applyNotchOptions,
        applyResampleOptions,
    )

    options: Dict = {}
    options["sites"]: List = projData.getSites()
    options["sampleFreqs"]: List[float] = projData.getSampleFreqs()
    options["start"]: Union[bool, str] = False
    options["stop"]: Union[bool, str] = False
    options["outputsite"]: str = ""
    options["polreverse"]: Union[bool, Dict[str, bool]] = False
    options["scale"]: Union[bool, Dict[str, float]] = False
    options["calibrate"]: bool = False
    options["normalise"]: bool = False
    options["filter"]: Dict = {}
    options["notch"]: List[float] = []
    options["resamp"]: Dict = {}
    options["interp"]: bool = False
    options["prepend"]: str = "proc"
    options["postpend"]: str = ""
    options = parseKeywords(options, kwargs)

    # print info
    text: List = ["Processing with options"]
    for op, val in options.items():
        text.append("\t{} = {}".format(op, val))
    projectBlock(text)

    if isinstance(options["sites"], str):
        options["sites"] = [options["sites"]]

    # outputting to another site
    if options["outputsite"] != "":
        projectText(
            "Preprocessed data will be saved to output site {}".format(
                options["outputsite"]
            )
        )
        # create the site
        projData.createSite(options["outputsite"])
        projData.refresh()
        outputSitePath = projData.getSiteData(options["outputsite"]).timePath

    # output naming
    outPre = options["prepend"] + "_" if options["prepend"] != "" else ""
    outPost = "_" + options["postpend"] if options["postpend"] != "" else ""
    if outPre == "" and outPost == "" and options["outputsite"] == "":
        outPre = "proc_"

    # create a data calibrator writer instance
    cal = getCalibrator(projData.calPath, projData.config)
    if options["calibrate"]:
        cal.printInfo()
    writer = TimeWriterInternal()

    # format dates
    if options["start"]:
        options["start"] = datetime.strptime(options["start"], "%Y-%m-%d %H:%M:%S")
    if options["stop"]:
        options["stop"] = datetime.strptime(options["stop"], "%Y-%m-%d %H:%M:%S")

    for site in options["sites"]:
        siteData = projData.getSiteData(site)
        siteData.printInfo()
        # loop over frequencies
        for sampleFreq in options["sampleFreqs"]:
            measurements = siteData.getMeasurements(sampleFreq)
            if len(measurements) == 0:
                # no data files at this sample rate
                continue

            # otherwise, process
            for meas in measurements:
                # get the reader
                projectText("Processing site {}, measurement {}".format(site, meas))
                reader = siteData.getMeasurement(meas)
                startTime = reader.getStartDatetime()
                stopTime = reader.getStopDatetime()
                if (options["start"] or options["stop"]) and not checkDateOptions(
                    options, startTime, stopTime
                ):
                    continue
                # if the data contributes, copy in the data if relevant
                if options["start"]:
                    startTime = options["start"]
                if options["stop"]:
                    stopTime = options["stop"]

                # calculate the samples
                sampleStart, sampleEnd = reader.time2sample(startTime, stopTime)
                # now get the data
                timeData = reader.getPhysicalSamples(
                    startSample=sampleStart, endSample=sampleEnd
                )
                timeData.printInfo()
                headers = reader.getHeaders()
                chanHeaders, _ = reader.getChanHeaders()

                # apply options
                applyPolarisationReversalOptions(options, timeData)
                applyScaleOptions(options, timeData)
                applyCalibrationOptions(options, cal, timeData, reader)
                applyFilterOptions(options, timeData)
                applyNotchOptions(options, timeData)
                applyInterpolationOptions(options, timeData)
                applyResampleOptions(options, timeData)
                applyNormaliseOptions(options, timeData)

                # output dataset path
                if options["outputsite"] != "":
                    timePath = outputSitePath
                else:
                    timePath = siteData.timePath
                outPath = os.path.join(timePath, "{}{}{}".format(outPre, meas, outPost))
                # write time data - need to manually change some headers (hence the keywords)
                writer = TimeWriterInternal()
                writer.setOutPath(outPath)
                writer.writeData(
                    headers,
                    chanHeaders,
                    timeData,
                    start_time=timeData.startTime.strftime("%H:%M:%S.%f"),
                    start_date=timeData.startTime.strftime("%Y-%m-%d"),
                    stop_time=timeData.stopTime.strftime("%H:%M:%S.%f"),
                    stop_date=timeData.stopTime.strftime("%Y-%m-%d"),
                    numSamples=timeData.numSamples,
                    sample_freq=timeData.sampleFreq,
                    physical=True,
                )
                writer.printInfo()


def viewTime(
    projData: ProjectData, startDate: str, endDate: str, **kwargs
) -> Union[Figure, None]:
    """View timeseries in the project

    Parameters
    ----------
    projData : ProjectData
        The project data instance
    startDate : str
        The start of the data range to plot
    endDate : str
        The end of the date range to plot
    sites : List[str], optional
        List of sites 
    sampleFreqs : List[float], optional
        List of sample frequencies to plot
    chans : List[str], optional
        List of channels to plot
    polreverse :  Dict[str, bool]
        Keys are channels and values are boolean flags for reversing   
    scale : Dict[str, float]
        Keys are channels and values are floats to multiply the channel data by   
    calibrate : bool, optional
        Boolean flag to calibrate data
    normalise : bool, optional
        Boolean flag to normalise the data. Default is False and setting to True will normalise each channel independently.
    notch : List[float], optional
        List of frequencies to notch out
    filter : Dict, optional
        Filter parameters
    show : bool, optional
        Boolean flag to show the plot
    save : bool, optional
        Boolean flag to save the plot to images folder
    plotoptions : Dict
        Dictionary of plot options

    Returns
    -------
    matplotlib.pyplot.figure or None
        A matplotlib figure unless the plot is not shown and is saved, in which case None and the figure is closed.
    """
    from resistics.project.shortcuts import getCalibrator
    from resistics.project.preprocess import (
        applyPolarisationReversalOptions,
        applyScaleOptions,
        applyCalibrationOptions,
        applyFilterOptions,
        applyNormaliseOptions,
        applyNotchOptions,
    )
    from resistics.common.plot import savePlot, plotOptionsTime

    options = {}
    options["sites"]: List[str] = projData.sites
    options["sampleFreqs"]: Union[List[float], List[str]] = projData.getSampleFreqs()
    options["chans"]: List[str] = ["Ex", "Ey", "Hx", "Hy", "Hz"]
    options["polreverse"]: Union[bool, Dict[str, bool]] = False
    options["scale"]: Union[bool, Dict[str, float]] = False
    options["calibrate"]: bool = False
    options["normalise"]: bool = False
    options["filter"]: Dict = {}
    options["notch"]: List[float] = []
    options["show"]: bool = True
    options["save"]: bool = False
    options["plotoptions"]: Dict = plotOptionsTime()
    options = parseKeywords(options, kwargs)

    # prepare calibrator
    cal = getCalibrator(projData.calPath, projData.config)
    if options["calibrate"]:
        cal.printInfo()

    # format startDate and endDate
    start = datetime.strptime("{}.000".format(startDate), "%Y-%m-%d %H:%M:%S.%f")
    stop = datetime.strptime("{}.000".format(endDate), "%Y-%m-%d %H:%M:%S.%f")
    # collect relevant data - dictionary to store timeData
    timeDataAll = {}
    for site in options["sites"]:
        siteData = projData.getSiteData(site)
        if isinstance(siteData, bool):
            # site does not exist
            continue
        siteData.printInfo()
        measurements = siteData.getMeasurements()
        timeDataAll[site] = {}

        # loop over measurements and save data for each one
        for meas in measurements:
            sampleFreq = siteData.getMeasurementSampleFreq(meas)
            if sampleFreq not in options["sampleFreqs"]:
                continue

            # check if data contributes to user defined time period
            siteStart = siteData.getMeasurementStart(meas)
            siteStop = siteData.getMeasurementEnd(meas)
            if siteStop < start or siteStart > stop:
                continue

            reader = siteData.getMeasurement(meas)
            # get the samples of the datetimes
            sampleStart, sampleStop = reader.time2sample(start, stop)
            # as the samples returned from time2sample are rounded use sample2time to get the appropriate start and end times for those samples
            readStart, readStop = reader.sample2time(sampleStart, sampleStop)
            # get the data for any available channels meaning even those sites with missing channels can be plotted
            timeData = reader.getPhysicalData(readStart, readStop)

            projectText(
                "Plotting measurement {} of site {} between {} and {}".format(
                    meas, site, readStart, readStop
                )
            )

            # apply various options
            applyPolarisationReversalOptions(options, timeData)
            applyScaleOptions(options, timeData)
            applyCalibrationOptions(options, cal, timeData, reader)
            applyFilterOptions(options, timeData)
            applyNotchOptions(options, timeData)
            applyNormaliseOptions(options, timeData)
            timeDataAll[site][meas] = timeData

    # plot all the data
    plotfonts = options["plotoptions"]["plotfonts"]
    fig = plt.figure(figsize=options["plotoptions"]["figsize"])
    for site in timeDataAll:
        for meas in timeDataAll[site]:
            timeData = timeDataAll[site][meas]
            timeData.view(
                sampleStop=timeDataAll[site][meas].numSamples - 1,
                fig=fig,
                chans=options["chans"],
                label="{} - {}".format(site, meas),
                xlim=[start, stop],
                plotfonts=plotfonts,
            )

    # add the suptitle
    st = fig.suptitle(
        "Time data from {} to {}".format(
            start.strftime("%Y-%m-%d %H-%M-%S"), stop.strftime("%Y-%m-%d %H-%M-%S")
        ),
        fontsize=plotfonts["suptitle"],
    )
    st.set_y(0.98)

    # do the axis labels
    numChans = len(options["chans"])
    for idx, chan in enumerate(options["chans"]):
        plt.subplot(numChans, 1, idx + 1)
        # do the yaxis
        if isElectric(chan):
            plt.ylabel("mV/km", fontsize=plotfonts["axisLabel"])
            if len(options["plotoptions"]["Eylim"]) > 0:
                plt.ylim(options["plotoptions"]["Eylim"])
        else:
            if options["calibrate"]:
                plt.ylabel("nT", fontsize=plotfonts["axisLabel"])
            else:
                plt.ylabel("mV", fontsize=plotfonts["axisLabel"])
            if len(options["plotoptions"]["Hylim"]) > 0:
                plt.ylim(options["plotoptions"]["Hylim"])
        plt.legend(loc=1, fontsize=plotfonts["legend"])

    # plot format
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    fig.subplots_adjust(top=0.92)

    # plot show and save
    if options["save"]:
        impath = projData.imagePath
        filename = "timeData_{}_{}".format(
            start.strftime("%Y-%m-%d_%H-%M-%S_"), stop.strftime("%Y-%m-%d_%H-%M-%S")
        )
        savename = savePlot(impath, filename, fig)
        projectText("Image saved to file {}".format(savename))
    if options["show"]:
        plt.show(block=options["plotoptions"]["block"])
    if not options["show"] and options["save"]:
        plt.close(fig)
        return None
    return fig
