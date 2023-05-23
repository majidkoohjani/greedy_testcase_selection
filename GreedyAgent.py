import pandas as pd
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
        self.__warmup: int = warmup

    def __sortRanks(self) -> None:
        self.__testCasesRank = Helper.sortDictionaryByValue(self.__testCasesRank)

    def __updateRanks(self, currentCycle: int) -> None:
        if self.__warmup < 1:
            for record in self.__testCasesHistory:
                self.__testCasesRank.update({
                    record: float("%.2f" % (self.__testCasesHistory[record]["fails"] / self.__testCasesHistory[record]["runs"]))
                })
            self.__sortRanks()
            self.__setRecommendations(currentCycle)
        else:
            self.__warmup -= 1

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

    def __setRecommendations(self, cycleID: int) -> None:
        topN: dict = Helper.takeFirstNFromDict(self.__recommendsPerCycle, self.__testCasesRank)

        self.__recommendation.update({
            cycleID: topN
        })

    def getRecommendations(self) -> dict:
        return self.__recommendation

    def run(self) -> None:
        groupedData = self.__testCases.groupby("Cycle")

        print("Operation started...")

        for cycle in self.__cycles:
            cycleTestCases: DataFrame = groupedData.get_group(cycle)

            self.__updateRanks(currentCycle=cycle)
            self.__updateHistory(cycleTestCases)

        self.__updateRanks(currentCycle=self.__cycles[-1])

        print("Operation finished successfully ;)")
