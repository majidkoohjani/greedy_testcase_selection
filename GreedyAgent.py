from pandas import DataFrame
from Helper import Helper

class GreedyAgent:
    """
    @cyclesList: لیستی از شناسه چرخه های موجود در دیتاست
    
    @testCases: تمام دیتاست

    @warmup: تعداد سیکل های که باید رد شویم و فقط از آن ها برای پر کردن تاریخچه استفاده کنیم

    @recommendsPerCycle: تعداد پیشنهادهای الگوریتم ما برای اجرا در سیکل بعد
    """
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
        self.__recommendsToCycleTestCases: list = []
        self.__recommendationFinal: dict = {}
        self.__apfds: list = []
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

    def __setRatio(self, cycleID: int, ratio: float = 0.0) -> None:
        self.__ratio.append((cycleID, ratio))

    def __setRecommendationFinal(self, currentCycleID: int, cycleTestCases: DataFrame) -> None:
        ourRecommendation = set(str(x) for x in self.__recommendation[currentCycleID].keys())

        temp = {}

        for item in ourRecommendation:
            foundRecords = cycleTestCases.query(f"Name == {item}")

            if not foundRecords.empty:
                verdict = 0 if foundRecords.query("Verdict == 1").empty else 1

                temp.update({
                    item: verdict
                })

        # for index, row in cycleTestCases.iterrows():
        #     if str(row["Name"]) in ourRecommendation:
        #         temp.update({
        #             row["Name"]: row["Verdict"]
        #         })

        self.__recommendationFinal.update({
            currentCycleID: temp
        })

    def __setRecommendsToCycleTestCases(self, cycleID: int, ratio: float = 0.0) -> None:
        self.__recommendsToCycleTestCases.append((cycleID, ratio))

    def __setRecommendations(self, cycleID: int) -> None:
        topN: dict = Helper.takeNTopRanksFromDict(self.__testCasesRank)

        self.__recommendation.update({
            cycleID: topN
        })

    # Check that how many records of our recommendation list match really failed test-cases in a cycle
    def __setTruePositives(self, currentCycleID: int, realFailedTestCases: set) -> None:
        realFailedTestCases = set(str(x) for x in realFailedTestCases)
        ourRecommendation = set(str(x) for x in self.__recommendation[currentCycleID].keys())

        matched = list(ourRecommendation.intersection(realFailedTestCases))
        precision: float = 0
        
        if len(matched) > 0:
            precision = float("%.3f" % (len(matched) / len(realFailedTestCases)))

        self.__truePositives[currentCycleID] = {
            "recall": precision,
            "matched": matched
        }
        
        self.__setRatio(currentCycleID, precision)

    def __recommendsToCycleTestCasesRatio(self, currentCycleID: int, cycleTestCases: set) -> None:
        cycleTestCases = set(str(x) for x in cycleTestCases)
        ourRecommendation = set(str(x) for x in self.__recommendation[currentCycleID].keys())

        matched = list(ourRecommendation.intersection(cycleTestCases))
        result: float = 0
        
        if len(matched) > 0:
            result = float("%.3f" % (len(matched) / len(cycleTestCases)))

        self.__setRecommendsToCycleTestCases(currentCycleID, result)

    def __setFailsToAllRatio(self, cycleID: int, ratio: float = 0.0) -> None:
        self.__failsToAllRatio.append((cycleID, ratio))

    def __calculateNRPA(self):
        pass

    # APFD = 1 - (((TF1 + TF2 + ... + TFn) / (n*m)) + (1/(2*n)))
    # N = testcases no
    # M = fails no
    def __calculateAPFD(self, n: int, m: int, currentCycle: int) -> None:
        sumTFn: float = 0
        apfd: float = 0

        i: int = 1
        for item in self.__recommendationFinal[currentCycle]:
            sumTFn += self.__recommendationFinal[currentCycle][item] * i
            i += 1

        if n > 0 and m > 0:
            apfd = 1 - ((sumTFn / (n * m)) + (1 / (2 * n)))

        self.__apfds.append(apfd)

    # Public functions
    def getRecommendationFinal(self) -> dict:
        return self.__recommendationFinal
    
    def getAPFDs(self) -> list:
        return self.__apfds;
    
    def getRatio(self) -> list:
        return self.__ratio
    
    def getFailsToAllRatio(self) -> list:
        return self.__failsToAllRatio
    
    def getRecommendsToCycleTestCases(self) -> list:
        return self.__recommendsToCycleTestCases
    
    def getRecommendations(self) -> dict:
        return self.__recommendation 

    def getTruePositives(self) -> dict:
        return self.__truePositives
    
    """
    تابع اصلی کلاس
    """
    def run(self) -> None:
        groupedData = self.__testCases.groupby("Cycle")

        print("Operation started...")
        
        failedTestCases: set = {}
        allTestCases: set = {}

        for cycle in self.__cycles:
            cycleTestCases: DataFrame = groupedData.get_group(cycle)
            failedTestCases = set(cycleTestCases.loc[cycleTestCases["Verdict"] == 1]["Name"].values.tolist())
            allTestCases = set(cycleTestCases["Name"].values.tolist())

            if (len(allTestCases) < 6):
                self.__updateHistory(cycleTestCases)
                continue

            self.__setFailsToAllRatio(cycleID=cycle, ratio=float("%.3f" % (len(failedTestCases) / len(allTestCases))))

            if self.__updateRanks(currentCycle=cycle):
                self.__setTruePositives(currentCycleID=cycle, realFailedTestCases=failedTestCases)
                self.__recommendsToCycleTestCasesRatio(currentCycleID=cycle, cycleTestCases=allTestCases)
                self.__setRecommendationFinal(currentCycleID=cycle, cycleTestCases= cycleTestCases)
            
            self.__updateHistory(cycleTestCases)

            if cycle == self.__cycles[-1]:
                if self.__updateRanks(currentCycle=cycle):
                    self.__setTruePositives(currentCycleID=cycle, realFailedTestCases=failedTestCases)
                    self.__recommendsToCycleTestCasesRatio(currentCycleID=cycle, cycleTestCases=allTestCases)
                    self.__setRecommendationFinal(currentCycleID=cycle, cycleTestCases= cycleTestCases)

            if (len(self.__recommendationFinal) > 0):
                self.__calculateAPFD(n=len(allTestCases), m=len(failedTestCases), currentCycle=cycle)

        print("Operation finished successfully ;)")
