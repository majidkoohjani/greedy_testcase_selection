from pandas import DataFrame
from DataLoader import DataLoader
from DatasetMetaData import DatasetMetaData
from GreedyAgent import GreedyAgent
from Plotter import Plotter

if __name__ == "__main__":
    # * Just load data from dataset
    dataLoader = DataLoader()
    loadedDataset: DataFrame = dataLoader.getReadyData()
    groupedDataByCycleID = loadedDataset.groupby("Cycle")
    groupedDataByTestCasesID = loadedDataset.groupby("Name")

    # * Extract needed data from dataset and cycles and test-cases
    metaDataExtractor = DatasetMetaData(loadedDataset)
    cycleIDs: list = metaDataExtractor.getListOfCycleIDs()
    
    # * Greedy agent
    agent = GreedyAgent(cyclesList=cycleIDs, testCases=loadedDataset)
    agent.run()
    # results = agent.getRecommendations()
    # tp = agent.getTruePositives()

    # dataLoader.saveResultsAsJson(results, "recommendations")
    # dataLoader.saveResultsAsJson(tp, "tp")

    ratio: list = agent.getRatio()
    ratioX: list = [x for x, y in ratio]
    ratioY: list = [y for x, y in ratio]

    failedToAllRatio: list = agent.getFailsToAllRatio()
    failedToAllRatioX: list = [x for x, y in failedToAllRatio]
    failedToAllRatioY: list = [y for x, y in failedToAllRatio]

    recommendsToCycleTestCases: list = agent.getRecommendsToCycleTestCases()
    recommendsToCycleTestCasesX: list = [x for x, y in recommendsToCycleTestCases]
    recommendsToCycleTestCasesY: list = [y for x, y in recommendsToCycleTestCases]

    # * Plotting
    dataToBePlotted: list = [
        {
            "x": ratioX, 
            "y": ratioY, 
            "title": "Recommends/realFails ratio", 
            "xLabel": "Cycles", 
            "yLabel": "recommends/realFails", 
            "color": "red", 
            "ls": "solid", 
            "lw": 1
        },
        {
            "x": failedToAllRatioX, 
            "y": failedToAllRatioY, 
            "title": "fails/all in each cycle", 
            "xLabel": "Cycles", 
            "yLabel": "fails/all", 
            "color": "blue", 
            "ls": "dotted", 
            "lw": 1
        },
        {
            "x": recommendsToCycleTestCasesX, 
            "y": recommendsToCycleTestCasesY, 
            "title": "recommends with cycle`s Test cases/cycle`s Test cases in each cycle", 
            "xLabel": "Cycles", 
            "yLabel": "ratio", 
            "color": "orange", 
            "ls": "dashed", 
            "lw": 1
        },
    ]

    Plotter.plotLine(multiLinePlot=dataToBePlotted, title="Ratio", xLabel="Cycles", yLabel="Ratio")
    Plotter.plotSubplot(multiPlot=dataToBePlotted)
