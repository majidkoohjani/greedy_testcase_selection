from pandas import DataFrame
from itertools import islice

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
