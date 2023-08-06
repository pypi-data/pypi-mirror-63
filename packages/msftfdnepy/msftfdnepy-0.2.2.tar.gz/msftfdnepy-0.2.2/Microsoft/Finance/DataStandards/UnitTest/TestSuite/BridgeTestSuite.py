from Microsoft.Finance.DataStandards.UnitTest.TestCase.BridgeTestCase import BridgeTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestCase.CommonTestCase import CommonTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BaseTestSuite import BaseTestSuite
from pyspark.sql.session import SparkSession
from unittest import TestLoader

class BridgeTestSuite(BaseTestSuite):

    #region Constructor

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str):
        super(BridgeTestSuite, self).__init__(sparkSession, databaseName, tableName)

    #endregion

    #region Class Methods

    def queue_tests(self) -> None:

        loader = TestLoader()

        names = loader.getTestCaseNames(BridgeTestCase)

        for name in names:
            self.TestSuite.addTest(BridgeTestCase(self.FieldInfo, self.CustomEvents, name))

        names = loader.getTestCaseNames(CommonTestCase)

        for name in names:
            self.TestSuite.addTest(CommonTestCase(self.TableDataFrame, self.FieldInfo, self.CustomEvents, name))

    #endregion