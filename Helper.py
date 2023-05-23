from pandas import DataFrame

class Helper:
    @staticmethod
    def sortTestCasesBy(data: DataFrame, sortBy: str, ascending: bool = True) -> DataFrame:
        newColName: str = f"{sortBy}Count"
        data[newColName] = data[sortBy].str.len()

        result: DataFrame = data.sort_values(by=newColName, ascending=ascending).drop(columns=newColName)

        return result
