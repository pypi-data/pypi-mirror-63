from Microsoft.Finance.DataStandards.UnitTest.TestCase.BridgeTestCase import BridgeTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestCase.CommonTestCase import CommonTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BaseTestSuite import BaseTestSuite
from pyspark.sql.session import SparkSession

class TestSuiteBridge(BaseTestSuite):

    #region Constructor

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str):
        super(TestSuiteBridge, self).__init__(sparkSession, databaseName, tableName)

    #endregion

    #region Class Methods

    def queue_tests(self) -> None:
        bridgeTestCase = TestCaseBridge(self.FieldInfo, self.CustomEvents)
        commonTestCase = TestCaseCommon(self.TableDataFrame, self.FieldInfo, self.CustomEvents)
        self.TestSuite.addTest(bridgeTestCase)
        self.TestSuite.addTest(commonTestCase)

    def run_tests(self) -> None:
        self.TestRunner(self.TestSuite)

    #endregion