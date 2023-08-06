from Microsoft.Finance.DataStandards.UnitTest.TestCase.CommonTestCase import CommonTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestCase.DimensionTestCase import DimensionTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BaseTestSuite import BaseTestSuite
from pyspark.sql.session import SparkSession

class DimensionTestSuite(BaseTestSuite):

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str) -> None:
        super(DimensionTestSuite, self).__init__(sparkSession, databaseName, tableName)

    def queue_tests(self) -> None:
        dimensionTestCase = DimensionTestCase(self.SparkSession, self.FieldInfo, self.DatabaseName, self.TableName, self.TableCount, self.CustomEvents)
        commonTestCase = CommonTestCase(self.TableDataFrame, self.FieldInfo, self.CustomEvents)
        self.TestSuite.addTest(dimensionTestCase)
        self.TestSuite.addTest(commonTestCase)

    def run_tests(self) -> None:
        self.TestRunner.run(self.TestSuite)