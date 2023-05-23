from pandas import DataFrame
from DataLoader import DataLoader
from DatasetMetaData import DatasetMetaData
from GreedyAgent import GreedyAgent
import json

if __name__ == "__main__":
    # * Just load data from dataset
    dataLoader = DataLoader()
    loadedDataset: DataFrame = dataLoader.getReadyData()
    groupedDataByCycleID = loadedDataset.groupby("Cycle")
    groupedDataByTestCasesID = loadedDataset.groupby("Name")

    # * Extract needed data from dataset and cycles and test-cases
    metaDataExtractor = DatasetMetaData(loadedDataset)
    cycleIDs: list = metaDataExtractor.getListOfCycleIDs()
    # numberOfCycles: int = metaDataExtractor.getNumberOfCycles()
    # numberOfTestcases: int = metaDataExtractor.getNumberOfAllTestCases()
    # firstCycleID: int = metaDataExtractor.getFirstCycle()
    # lastCycleID: int = metaDataExtractor.getLastCycle()
    # firstTestCaseID: int = metaDataExtractor.getFirstTestCaseID()
    # lastTestCaseID: int = metaDataExtractor.getLastTestCaseID()
    # testCasesIDs: list = metaDataExtractor.getListOfTestCaseIDs()
    # testCaseFailures: int = metaDataExtractor.getTestCaseFailures(firstTestCaseID)
    # testCaseTotalRuns: int = metaDataExtractor.getTestCaseTotalRuns(firstTestCaseID)
    
    # Greedy agent
    agent = GreedyAgent(cyclesList=cycleIDs, testCases=loadedDataset)
    agent.run()
    results = agent.getRecommendations()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # * Variables print for test
    # print(testCaseFailures, testCaseTotalRuns)
