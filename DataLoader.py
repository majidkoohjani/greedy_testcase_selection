import os
import pandas

class DataLoader:
    __experimentsBaseFolder = "./experiments"

    def __init__(self) -> None:
        self.__DATASET = "./datasets/iofrol-additional-features.csv"
    
    # Just used whenever we wanna check for a folder and create it if not exists
    def __checkOrCreatePath(self, pathToCheck: str = ""):
        if not type(pathToCheck) is str or len(pathToCheck) < 1:
            raise Exception("1000: Check pathToCheck parameter again, it`s empty or wrong type!!!")
        
        if not os.path.exists(pathToCheck):
            os.makedirs(pathToCheck)

    # Get dataset name for path
    def __getDatasetName(self, datasetPath: str = "") -> str:
        if not type(datasetPath) is str or len(datasetPath) < 1:
            raise Exception("1001: Check datasetPath parameter again, it`s empty or wrong type!!!")
        
        finalDataPath = datasetPath.strip()

        if finalDataPath.endswith("/"):
            finalDataPath = finalDataPath[:-1]
        
        lastSlashIndex = finalDataPath.rfind("/")

        if lastSlashIndex < 0:
            raise Exception("1002: It seems dataset path is wrong!!!")
        else:
            fileName = finalDataPath[lastSlashIndex + 1:]
            extensionDotIndex = fileName.rfind(".")

            return fileName if extensionDotIndex == -1 else fileName[0: extensionDotIndex]
        

    # Load data from it`s .csv file using pandas library
    def __loadData(self, dataPath: str):
        dataFrame = pandas.read_csv(dataPath, sep = ',')

        return dataFrame

    # Just do load and preprocess together to avoid separate function calls
    def __loadAndPreprocessData(self, dataPath: str):
        dataFrame = self.__loadData(dataPath)

        # Preprocess function is not implemented yet!!! It seems it's not needed.

        return dataFrame
    
    def getReadyData(self):
        finalOutputPath = f"{self.__experimentsBaseFolder}/{self.__getDatasetName(self.__DATASET)}"

        self.__checkOrCreatePath(finalOutputPath)
        
        return self.__loadAndPreprocessData(self.__DATASET)
    
    def publicGetDatasetName(self) -> str:
        return self.__getDatasetName(self.__DATASET)
