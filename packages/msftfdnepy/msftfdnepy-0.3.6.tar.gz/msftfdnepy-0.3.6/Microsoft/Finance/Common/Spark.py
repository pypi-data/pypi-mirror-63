from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from typing import Set

class Spark(object):

    #region Constructor
    
    def __init__(self, sparkSession):
        self.__sparkSession = sparkSession
    
    #endregion

    #region Properties

    @property
    def Session(self):
        return self.__sparkSession

    #endregion

    #region Static Methods

    @staticmethod
    def get_single_row_result(df: DataFrame) -> object:

        if not df:
            raise ValueError("data frame cannot be None...")
    
        firstColumnName = df.schema.fields[0].name
        result = df.select(firstColumnName)
    
        return result

    @staticmethod
    def get_distinct_column_values_from_df(df: DataFrame, columnName: str) -> Set:

        if not df:
            raise ValueError("data frame cannot be None...")

        if not columnName:
            raise ValueError("column name cannot be None or empty...")

        values = set([row[0] for row in df.select(columnName).distinct().collect()])

        return values

    @staticmethod
    def get_field_info(df: DataFrame) -> [(str, type)]:

        if not df:
            raise ValueError("data frame cannot be None...")

        fieldInfo = [ (field.name, field.dataType) for field in df.schema.fields ]

        return fieldInfo

    #endregion

    #region Class Methods

    def get_databases(self) -> [str]:
        
        query = "show databases"
        df = spark.sql(query)
        dbs = [db[0] for db in df.select("databaseName").distinct().collect()]
        
        return dbs

    def get_tables(self, databaseName: str) -> [str]:
        
        query = "show tables in {}".format(databaseName)
        df = self.evaluate_query(query)
        tables = [row[0] for row in df.select("tableName").distinct().collect()]
        
        return tables

    def get_tables_by_database(self) -> {str: [str]}:
        
        tablesByDb = {}
        dbs = self.get_databases()
        
        for db in dbs:
            tables = self.get_tables(db)
            tablesByDb[db] = tables
        
        return tablesByDb

    def evaluate_query(self, query: str) -> DataFrame:

        if not query:
            raise ValueError("query cannot be None or empty...")
        
        try:
            df = self.__sparkSession.sql(query)
            return df
        except Exception as ex:
            raise ex

    def get_table_or_view(self, databaseName: str, tableName: str) -> DataFrame:

        if not databaseName:
            raise ValueError("database name cannot be None or empty...")

        if not tableName:
            raise ValueError("table name cannot be None or empty...")

        tableQuery = "select * from {}.{}".format(databaseName, tableName)

        df = self.evaluate_query(tableQuery)

        return df

    def count_table_or_view(self, databaseName: str, tableName: str) -> int:

        if not databaseName:
            raise ValueError("database name cannot be None or empty...")

        if not tableName:
            raise ValueError("table name cannot be None or empty...")

        countQuery = "select count(1) from {}.{}".format(databaseName, tableName)
        
        df = self.evaluate_query(countQuery)

        count = self.get_single_row_result(df)

        return count

    def count_distinct_column_values(self, databaseName: str, tableName: str, columnName: str) -> int:

        if not databaseName:
            raise ValueError("database name cannot be None or empty...")

        if not tableName:
            raise ValueError("table name cannot be None or empty...")

        if not columnName:
            raise ValueError("column name cannot be None or empty...")

        countQuery = "select count(1) from (select distinct {} from {}.{})".format(columnName, databaseName, tableName)
    
        df = self.evaluate_query(countQuery)
        
        count = self.get_single_row_result(df)

        return count
    
    def get_distinct_column_values(self, databaseName: str, tableName: str, columnName: str) -> Set:

        if not databaseName:
            raise ValueError("database name cannot be None or empty...")

        if not tableName:
            raise ValueError("table name cannot be None or empty...")

        if not columnName:
            raise ValueError("column name cannot be None or empty...")

        columnQuery = "select {} from {}.{}".format(columnName, databaseName, tableName)

        df = self.evaluate_query(columnQuery)

        distinctValues = self.get_distinct_column_values_from_df(df, columnName)

        return distinctValues

    def count_query(self, query: str) -> int:

        if not query:
            raise ValueError("query cannot be None or empty...")

        countQuery = "select count(1) from ( {} )".format(query)

        df = self.evaluate_query(countQuery)

        count = self.get_single_row_result(df)

        return count

    def get_field_info_from_query(self, query: str) -> [(str, type)]:

        if not query:
            raise ValueError("query cannot be None or empty...")

        df = self.evaluate_query(query)
        
        fieldInfo = self.get_field_info(df)
        
        return fieldInfo

    def get_field_info_table_or_view(self, databaseName: str, tableName: str) -> [(str, type)]:

        if not databaseName:
            raise ValueError("database name cannot be None or empty...")

        if not tableName:
            raise ValueError("table name cannot be None or empty...")

        df = self.get_table_or_view(databaseName, tableName)
        
        fieldInfo = self.get_field_info(df)

        return fieldInfo

    #endregion