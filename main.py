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
    results = agent.getRecommendations()
    tp = agent.getTruePositives()

    dataLoader.saveResultsAsJson(results, "recommendations")
    dataLoader.saveResultsAsJson(tp, "tp")

    ratio: list = agent.getRatio()
    ratioX: list = [x for x, y in ratio]
    ratioY: list = [y for x, y in ratio]

    failedToAllRatio: list = agent.getFailsToAllRatio()
    failedToAllRatioX: list = [x for x, y in failedToAllRatio]
    failedToAllRatioY: list = [y for x, y in failedToAllRatio]

    # * Plotting
    dataToBePlotted: list = [
        {"x": ratioX, "y": ratioY, "title": "Recommends/realFails ratio", "xLabel": "Cycles", "yLabel": "recommends/realFails", "color": "red", "ls": "solid", "lw": 1},
        {"x": failedToAllRatioX, "y": failedToAllRatioY, "title": "fails/all in each cycle", "xLabel": "Cycles", "yLabel": "fails/all", "color": "blue", "ls": "dotted", "lw": 1},
    ]

    # Plotter.plot(multiLinePlot=dataToBePlotted, title="recommended/Real fails ratio", xLabel="CycleID", yLabel="Ratio")
    Plotter.plotInMultiPlot(multiPlot=dataToBePlotted)
