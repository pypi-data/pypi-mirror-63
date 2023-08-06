from Microsoft.Finance.DataStandards.UnitTest.TestCase.CommonTestCase import CommonTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BaseTestSuite import BaseTestSuite
from pyspark.sql.session import SparkSession
from unittest import TestLoader

class StagingTestSuite(BaseTestSuite):

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str) -> None:
        super(StagingTestSuite, self).__init__(sparkSession, databaseName, tableName)

    def queue_tests(self) -> None:

        loader = TestLoader()

        names = loader.getTestCaseNames(CommonTestCase)

        for name in names:
            self.TestSuite.addTest(CommonTestCase(self.TableDataFrame, self.FieldInfo, self.CustomEvents, name))
