from pandas import DataFrame

class DatasetMetaData:
    def __init__(self, data: DataFrame) -> None:
        self.__dataset: DataFrame = data
        self.__datasetGroupedByName = data.groupby("Name")
        self.__datasetGroupedByCycle = data.groupby("Cycle")

    def getNumberOfRows(self) -> int:
        return self.__dataset.shape[0]
    
    def getNumberOfColumns(self) -> int:
        return self.__dataset.shape[1]

    def getNumberOfCycles(self) -> int:
        groupedDataByCycleID = self.__datasetGroupedByCycle

        return len(groupedDataByCycleID)

    def getNumberOfAllTestCases(self) -> int:
        groupedDataByName = self.__datasetGroupedByName

        return len(groupedDataByName)
    
    def getFirstCycle(self) -> int:
        return self.__dataset["Cycle"].min()
        
    def getLastCycle(self) -> int:
        return self.__dataset["Cycle"].max()
    
    def getFirstTestCaseID(self) -> int:
        return self.__dataset["Name"].min()
    
    def getLastTestCaseID(self) -> int:
        return self.__dataset["Name"].max()
    
    def getTestCaseFailures(self, testCaseID: int) -> int:
        tempTestcases: DataFrame = self.__datasetGroupedByName.get_group(testCaseID)
        
        return tempTestcases.groupby("Verdict").get_group(0).shape[0]

    def getTestCaseTotalRuns(self, testCaseID: int) -> int:
        return self.__datasetGroupedByName.get_group(testCaseID).shape[0]

    def getListOfTestCaseIDs(self) -> list:
        return sorted(set(self.__dataset["Name"].values.tolist()))
    
    def getListOfCycleIDs(self) -> list:
        return sorted(set(self.__dataset["Cycle"].values.tolist()))
