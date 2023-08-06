import json
from Microsoft.Finance.Common.Spark import Spark

class TestObject(object):

    #region Constructor
    
    def __init__(self, name: str, database: str, correlationId: int):
        self.__name = name
        self.__database = database
        self.__correlationId = correlationId
        self.__rowCountBefore = -1
        self.__rowCountAfter = -1
    
    #endregion

    #region Properties

    @property
    def Database(self):
        return self.__database

    @property
    def CorrelationId(self):
        return self.__correlationId

    @property
    def Name(self):
        return self.__name

    @property
    def Type(self):
        if self.__name[0:4] == "dim_":
            return "dimension"
        elif self.__name[0:5] == "fact_":
            return "fact"
        elif self.__name[0:7] == "bridge_":
            return "bridge"
        else:
            return "staging"

    #endregion

    #region Class Methods

    def __str__(self):

        d = {}

        d["name"] = self.__name
        d["database"] = self.__database
        d["type"] = self.Type
        d["row_count_before"] = self.__rowCountBefore
        d["row_count_after"] = self.__rowCountAfter

        return json.dumps(d)

    def set_row_count_before(self, spark: Spark = None, rowCount = -1):

        if rowCount >= 0:
            self.__rowCountBefore = rowCount
        else:
            self.get_row_count(spark)

    def set_row_count_after(self, spark: Spark = None, rowCount = -1):

        if rowCount >= 0:
            self.__rowCountBefore = rowCount
        else:
            self.get_row_count(spark, False)

    def get_row_count(self, spark: Spark, before: bool = True):

        if not spark:
            raise ValueError("spark utility cannot be None...")

        rowCount = spark.count_table_or_view(self.__database, self.__name)

        if before:
            self.__rowCountBefore = rowCount
        else:
            self.__rowCountAfter = rowCount

    #endregion