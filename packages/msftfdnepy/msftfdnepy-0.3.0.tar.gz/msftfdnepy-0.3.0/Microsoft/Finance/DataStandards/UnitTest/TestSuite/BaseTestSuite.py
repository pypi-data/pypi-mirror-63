from datetime import datetime, timedelta
from json import dumps
from Microsoft.Finance.Common.Spark import Spark
from pyspark.sql.session import SparkSession
from pyspark.sql.dataframe import DataFrame
from unittest import TestSuite, TextTestRunner, TestLoader

class BaseTestSuite(object):

    #region Constructor

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str) -> None:
        self.__spark = Spark(sparkSession)
        self.__databaseName = databaseName
        self.__tableName = tableName
        self.__customEvents = []
        self.__tableCount = None
        self.__tableDataFrame = None
        self.__fieldInfo = None
        self.__duration = None
        self.__testSuite = TestSuite()
        self.__testRunner = TextTestRunner()

    #endregion

    #region Properties

    @property
    def TestRunner(self) -> TextTestRunner:
        return self.__testRunner
    
    @property
    def SparkUtility(self) -> Spark:
        return self.__spark

    @property
    def DatabaseName(self) -> str:
        return self.__databaseName

    @property
    def TableName(self) -> str:
        return self.__tableName

    @property
    def CustomEvents(self) -> {}:
        return self.__customEvents

    @property
    def TestSuite(self) -> TestSuite:
        return self.__testSuite

    @property
    def TableCount(self) -> int:
        if not self.__tableCount:
            self.__tableCount = self.__spark.count_table_or_view(self.__databaseName, self.__tableName)
        return self.__tableCount

    @property
    def TableDataFrame(self) -> DataFrame:
        if not self.__tableDataFrame:
            self.__tableDataFrame = self.__spark.get_table_or_view(self.__databaseName, self.__tableName)
        return self.__tableDataFrame

    @property
    def FieldInfo(self) -> [(str, type)]:
        if not self.__fieldInfo:
            self.__fieldInfo = self.__spark.get_field_info(self.TableDataFrame)
        return self.__fieldInfo

    @property 
    def SuiteDurationSeconds(self) -> float:
        if not __customEvents:
            return 0.0
        else:
            if not self.__duration:
                self.__duration = sum([event.EventDurationSeconds for event in self.__customEvents])
            return self.__duration.total_seconds()

    @property
    def SuiteDurationMilliseconds(self) -> float:
        return self.SuiteDurationSeconds * 1000

    #endregion

    #region Class Methods

    def __str__(self) -> str:
        s = dumps(self.__dict__)
        return s

    def dump_events(self) -> None:

        for event in self.CustomEvents:
            print("Event Name: {}\nEvent Details: {}".format(event.TestName, str(event)))
    
    def run_tests(self) -> None:

        print("TEST RESULTS")

        self.TestRunner.run(self.TestSuite)

        print("\nEVENT DETAILS")

        self.dump_events()

    #endregion
