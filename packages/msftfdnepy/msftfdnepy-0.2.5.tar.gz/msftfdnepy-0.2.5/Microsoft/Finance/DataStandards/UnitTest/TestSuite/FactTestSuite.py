from Microsoft.Finance.DataStandards.UnitTest.TestCase.CommonTestCase import CommonTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestCase.FactTestCase import FactTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BaseTestSuite import BaseTestSuite
from pyspark.sql.session import SparkSession
from unittest import TestLoader

class FactTestSuite(BaseTestSuite):

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str, linkedDimensions: [(str, str)], excludeFromAggregation: [str] = []):
        super(FactTestSuite, self).__init__(sparkSession, databaseName, tableName)
        self.__linkedDimensions = linkedDimensions
        self.__excludeFromAggregation = excludeFromAggregation

    def queue_tests(self) -> None:

        loader = TestLoader()

        names = loader.getTestCaseNames(FactTestCase)

        for name in names:
            self.TestSuite.addTest(FactTestCase(self.SparkSession, self.TableDataFrame, self.FieldInfo, self.__linkedDimensions, self.DatabaseName, self.TableName, self.TableCount, self.CustomEvents, self.__excludeFromAggregation))

        names = loader.getTestCaseNames(CommonTestCase)

        for name in names:
            self.TestSuite.addTest(CommonTestCase(self.TableDataFrame, self.FieldInfo, self.CustomEvents))
