from Microsoft.Finance.Common.DataBricks import Databricks
from Microsoft.Finance.Common.Spark import Spark
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

    def generate_standard_matrix(self, notebookPath: str, objects: [TestObject]) -> str:

        results = {}

        results["notebook_name"] = notebookPath

        # set rc for each object
        for obj in objects:
            obj.set_row_count_before(self.__spark)

        # execute notebook
        runId = self.__databricks.execute_notebook(notebookPath)
        executionTime = self.__databricks.get_run_execution_time(runId)

        results["execution_time"] = executionTime

        # set rc for each object
        for obj in objects:
            obj.set_row_count_after(self.__spark)

        # run tests
        for obj in objects:
            if obj.Type == "dimension":
                pass
            elif obj.Type == "fact":
                pass
            else:
                pass
        pass

    def generate_comprehensive_matrix(self, notebookPath: str, objects: [TestObject]) -> str:
        raise NotImplementedError("reserved by @phbennet")