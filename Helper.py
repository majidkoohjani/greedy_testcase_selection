from pandas import DataFrame
from itertools import islice
import time
import calendar

class Helper:
    @staticmethod
    def sortTestCasesBy(data: DataFrame, sortBy: str, ascending: bool = True) -> DataFrame:
        newColName: str = f"{sortBy}Count"
        data[newColName] = data[sortBy].str.len()

        result: DataFrame = data.sort_values(by=newColName, ascending=ascending).drop(columns=newColName)

        return result
    
    @staticmethod
    def sortDictionaryByValue(target: dict) -> dict:
        return dict(sorted(target.items(), key=lambda x:x[1], reverse=True))
    
    @staticmethod
    def takeFirstNFromDict(n: int, values: dict) -> dict:
        return dict(islice(values.items(), n))
    
    @staticmethod
    def takeNTopRanksFromDict(values: dict) -> dict:
        result: dict = {}

        for item in values:
            if float(values[item]) >= 1:
                result[item] = values[item]

        # for item in values:
        #     result[item] = values[item]

        return result
    
    @staticmethod
    def getTimeStamp() -> str:
        currentGMT = time.gmtime()
        timestamp = calendar.timegm(currentGMT)
        
        return str(timestamp)
