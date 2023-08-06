from Microsoft.Finance.DataStandards.UnitTest.TestCase.CommonTestCase import CommonTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestCase.FactTestCase import FactTestCase
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BaseTestSuite import BaseTestSuite
from pyspark.sql.session import SparkSession

class FactTestSuite(BaseTestSuite):

    def __init__(self, sparkSession: SparkSession, databaseName: str, tableName: str, linkedDimensions: [(str, str)], excludeFromAggregation: [str] = []):
        super(TestSuiteFact, self).__init__(sparkSession, databaseName, tableName)
        self.__linkedDimensions = linkedDimensions
        self.__excludeFromAggregations = excludeFromAggregations

    def queue_tests(self) -> None:
        factTestCase = FactTestCase(self.SparkSession, self.TableDataFrame, self.FieldInfo, self.__linkedDimensions, self.DatabaseName, self.TableName, self.TableCount, self.CustomEvents, self.__excludeFromAggregations)
        commonTestCase = CommonTestCase(self.TableDataFrame, self.FieldInfo, self.CustomEvents)
        self.TestSuite.addTest(factTestCase)
        self.TestSuite.addTest(commonTestCase)

    def run_tests(self) -> None:
        self.TestRunner.run(self.TestSuite)
