from typing import List

from resistics.common.print import generalPrint, warningPrint, errorPrint, blockPrint


class ResisticsBase(object):
    """Resistics base class
    
    Parent class to ensure consistency of print methods

    Methods
    -------
    __repr__()
        Print status information
    __str__()
        Print status information
    printInfo()
        Print status information
    printList()
        Return a list of strings with useful information
    printText(infoStr)
        Print information to console
    printWarning(warnStr)
        Print a warning to the console
    printError(errorStr, quitRun=False)
        Print an error to the console and optionally quit execution  
    """

    def __repr__(self) -> str:
        """Print class information"""
        return "\n".join(self.printList())

    def __str__(self) -> str:
        """Print class information"""
        return self.__repr__()

    def printInfo(self) -> None:
        """Print class information"""
        blockPrint(self.__class__.__name__, self.printList())

    def printList(self) -> List:
        """Class information as a list of strings

        Returns
        -------
        out : list
            List of strings with information
        """
        return [""]

    def printText(self, infoStr: str) -> None:
        """General print to terminal

        Parameters
        ----------
        infoStr : str
            The string to print to the console
        """
        generalPrint("{} Info".format(self.__class__.__name__), infoStr)

    def printWarning(self, warnStr: str) -> None:
        """Warning print to terminal
        
        Parameters
        ----------
        warnStr : str
            The string to print to the console
        """
        warningPrint("{} Warning".format(self.__class__.__name__), warnStr)

    def printError(self, errorStr: str, quitRun: bool = False) -> None:
        """Error print to terminal and possibly quit

        Parameters
        ----------
        errorStr : str
            The string to print to the console
        quitRun : bool, optional (False)
            If True, the code will exit
        """
        errorPrint(
            "{} Error".format(self.__class__.__name__), errorStr, quitRun=quitRun
        )
