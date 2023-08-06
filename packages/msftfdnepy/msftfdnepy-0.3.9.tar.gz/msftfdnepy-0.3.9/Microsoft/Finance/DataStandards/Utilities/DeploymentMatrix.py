from Microsoft.Finance.Common.DataBricks import Databricks
from Microsoft.Finance.Common.Spark import Spark
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.BridgeTestSuite import BridgeTestSuite
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.DimensionTestSuite import DimensionTestSuite
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.FactTestSuite import FactTestSuite
from Microsoft.Finance.DataStandards.UnitTest.TestSuite.StagingTestSuite import StagingTestSuite
from Microsoft.Finance.DataStandards.Utilities.TestUtilities import TestUtilities
from Microsoft.Finance.DataStandards.Utilities.TestObject import TestObject
from pyspark.sql.session import SparkSession

class DeploymentMatrix(object):

    def __init__(self, sparkSession: SparkSession, token: str, domain: str, clusterId: str):

        if not sparkSession:
            raise ValueError("spark session cannot be None...")

        if not token:
            raise ValueError("token cannot be None or empty...")

        if not domain:
            raise ValueError("domain cannot be None or empty...")

        if not clusterId:
            raise ValueError("cluster id cannot be None or empty...")

        self.__spark = Spark(sparkSession)
        self.__databricks = Databricks(token, domain, clusterId)

    def generate_standard_matrix(self, notebookPath: str, objects: [TestObject]) -> None:

        if not notebookPath:
            raise ValueError("notebook path cannot be None or empty...")

        if not objects:
            raise ValueError("test objects cannot be None or empty...")

        # set rc for each object
        for obj in objects:
            obj.set_row_count_before(self.__spark)

        # execute notebook
        runId = self.__databricks.execute_notebook(notebookPath)
        executionTime = self.__databricks.get_run_execution_time(runId)

        # set rc for each object
        for obj in objects:
            obj.set_row_count_after(self.__spark)

        session = self.__spark.Session

        print("Notebook Path: {}".format(notebookPath))
        print("Notebook Execution Time: {}".format(str(executionTime)))
        print("Notebook Run Id: {}".format(runId))

        # run tests
        for obj in objects:

            #print deployment meta data
            print("\nDEPLOYMENT METADATA")
            print(str(obj))

            #run appropriate test
            if obj.Type == "dimension":

                dimSuite = DimensionTestSuite(session, obj.Database, obj.Name)
                dimSuite.queue_tests()
                dimSuite.run_tests()

            elif obj.Type == "fact":

                #need to auto populate aggregation exclusions if possible
                linkedDims = [(o.Database, o.Name) for o in objects if o.CorrelationId == obj.CorrelationId]
                
                factSuite = FactTestSuite(session, obj.Database, obj.Name, linkedDims, [])
                factSuite.queue_tests()
                factSuite.run_tests()

            elif obj.Type == "bridge":

                bridgeSuite = BridgeTestSuite(session, obj.Database, obj.Name)
                bridgeSuite.queue_tests()
                bridgeSuite.run_tests()

            else:

                stagingSuite = StagingTestSuite(session, obj.Database, obj.Name)
                stagingSuite.queue_tests()
                stagingSuite.run_tests()