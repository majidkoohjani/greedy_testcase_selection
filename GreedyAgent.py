import pandas as pd
from pandas import DataFrame

class GreedyAgent:
    def __init__(self, cyclesList: list, testCases: DataFrame, warmup: int = 10) -> None:
        self.__cycles: list = cyclesList
        self.__testCases: DataFrame = testCases
        self.__testCasesHistory: dict = {}
        self.__testCasesRank: dict = {}
        self.__warmup: int = warmup

    def __updateRanks(self) -> None:
        if self.__warmup < 1:
            for record in self.__testCasesHistory:
                self.__testCasesRank.update({
                    record: {
                        "failsPerAll": float("%.2f" % (self.__testCasesHistory[record]["fails"] / self.__testCasesHistory[record]["runs"]))
                    }
                })
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

    def run(self) -> None:
        groupedData = self.__testCases.groupby("Cycle")

        for cycle in self.__cycles:
            cycleTestCases: DataFrame = groupedData.get_group(cycle)

            self.__updateRanks()
            self.__updateHistory(cycleTestCases)

        self.__updateRanks()

        print("Operation finished ;)")
