from pandas import DataFrame
from Helper import Helper

class GreedyAgent:
    def __init__(self, cyclesList: list, testCases: DataFrame, warmup: int = 10, recommendsPerCycle: int = 10) -> None:
        self.__cycles: list = cyclesList
        self.__testCases: DataFrame = testCases
        self.__testCasesHistory: dict = {}
        self.__testCasesRank: dict = {}
        self.__recommendation: dict = {}
        self.__recommendsPerCycle: int = recommendsPerCycle
        self.__truePositives: dict = {}
        self.__ratio: list = []
        self.__failsToAllRatio: list = []
        self.__warmup: int = warmup

    # Private functions
    def __sortRanks(self) -> None:
        self.__testCasesRank = Helper.sortDictionaryByValue(self.__testCasesRank)

    def __updateRanks(self, currentCycle: int) -> bool:
        returnFlag: bool = False

        if self.__warmup < 1:
            for record in self.__testCasesHistory:
                self.__testCasesRank.update({
                    record: float("%.3f" % (self.__testCasesHistory[record]["fails"] / self.__testCasesHistory[record]["runs"]))
                })
            self.__sortRanks()
            self.__setRecommendations(currentCycle)

            returnFlag = True
        else:
            self.__warmup -= 1
            self.__setRatio(currentCycle)

        return returnFlag

    def __updateHistory(self, selectedTestCases: DataFrame) -> None:
        for index, row in selectedTestCases.iterrows():
            testCaseID: str = str(row["Name"])
            lastFailsValue: int = 0
            lastRunsValue: int = 1

            if testCaseID in self.__testCasesHistory:
                lastFailsValue = self.__testCasesHistory[testCaseID]["fails"]
                lastRunsValue += self.__testCasesHistory[testCaseID]["runs"]

            if row["Verdict"] == 1:
                lastFailsValue += 1

            self.__testCasesHistory.update({
                testCaseID: {
                    "fails": lastFailsValue,
                    "runs": lastRunsValue
                }
            })

    def __setRatio(self, cycleID: int, precision: float = 0.0) -> None:
        self.__ratio.append((cycleID, precision))

    def __setRecommendations(self, cycleID: int) -> None:
        topN: dict = Helper.takeNTopRanksFromDict(self.__testCasesRank)

        self.__recommendation.update({
            cycleID: topN
        })

    # Check that how many records of our recommendation list match really failed test-cases in a cycle
    def __setTruePositives(self, currentCycleID: int, realFailedTestCases: set) -> None:
        realFailedTestCases = set(str(x) for x in realFailedTestCases)
        ourRecommendation = set(str(x) for x in self.__recommendation[currentCycleID].keys())

        matched = list(realFailedTestCases.intersection(ourRecommendation))
        precision = 0
        
        if len(matched) > 0:
            precision = float("%.3f" % (len(matched) / len(realFailedTestCases)))

        self.__truePositives[currentCycleID] = {
            "precision": precision,
            "matched": matched
        }
        
        self.__setRatio(currentCycleID, precision)

    def __setFailsToAllRatio(self, cycleID: int, ratio: float = 0.0) -> None:
        self.__failsToAllRatio.append((cycleID, ratio))

    # Public functions
    def getRatio(self) -> list:
        return self.__ratio
    
    def getFailsToAllRatio(self) -> list:
        return self.__failsToAllRatio
    
    def getRecommendations(self) -> dict:
        return self.__recommendation 

    def getTruePositives(self) -> dict:
        return self.__truePositives
    
    def run(self) -> None:
        groupedData = self.__testCases.groupby("Cycle")

        print("Operation started...")
        
        failedTestCases: set = {}
        allTestCases: set = {}

        for cycle in self.__cycles:
            cycleTestCases: DataFrame = groupedData.get_group(cycle)
            failedTestCases = set(cycleTestCases.loc[cycleTestCases["Verdict"] == 1]["Name"].values.tolist())
            allTestCases = set(cycleTestCases["Name"].values.tolist())

            self.__setFailsToAllRatio(cycleID=cycle, ratio=float("%.2f" % (len(failedTestCases) / len(allTestCases))))
            if self.__updateRanks(currentCycle=cycle):
                self.__setTruePositives(currentCycleID=cycle, realFailedTestCases=failedTestCases)
            self.__updateHistory(cycleTestCases)

        if self.__updateRanks(currentCycle=self.__cycles[-1]):
            self.__setTruePositives(currentCycleID=self.__cycles[-1], realFailedTestCases=failedTestCases)

        print("Operation finished successfully ;)")
