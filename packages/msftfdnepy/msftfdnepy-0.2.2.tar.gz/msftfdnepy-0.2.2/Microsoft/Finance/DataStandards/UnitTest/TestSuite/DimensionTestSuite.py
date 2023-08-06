from Microsoft.Finance.DataStandards.UnitTest.TestCase.CommonTestCase import CommonTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestCase.DimensionTestCase import DimensionTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BaseTestSuite import BaseTestSuite
from pyspark.sql.session import SparkSession
from unittest import TestLoader

class DimensionTestSuite(BaseTestSuite):

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str) -> None:
        super(DimensionTestSuite, self).__init__(sparkSession, databaseName, tableName)

    def queue_tests(self) -> None:

        loader = TestLoader()

        names = loader.getTestCaseNames(DimensionTestCase)

        for name in names:
            self.TestSuite.addTest(DimensionTestCase(self.SparkUtility, self.FieldInfo, self.DatabaseName, self.TableName, self.TableCount, self.CustomEvents, name))

        names = loader.getTestCaseNames(CommonTestCase)

        for name in names:
            self.TestSuite.addTest(CommonTestCase(self.TableDataFrame, self.FieldInfo, self.CustomEvents, name))