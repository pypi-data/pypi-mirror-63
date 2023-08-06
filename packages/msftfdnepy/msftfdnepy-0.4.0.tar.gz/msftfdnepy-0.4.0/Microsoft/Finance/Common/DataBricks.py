import json
import base64
import requests
import time
import uuid

class Databricks(object):

    #region Constructor

    def __init__(self, token: str, domain: str, clusterId: str = None):

        if not token:
            raise ValueError("token cannot be None or empty...")

        if not domain:
            raise ValueError("domain cannot be None or empty...")

        self.__domain = domain
        self.__token = token
        self.__uri = "https://{}.azuredatabricks.net/api/2.0".format(self.__domain)
        self.__header = { "Authorization": "Bearer {}".format(self.__token) }
        self.__clusterId = clusterId
    
    #endregion

    #region Class Methods

    def build_uri(self, endpoint: str, extension: str) -> str:

        if not endpoint:
            raise ValueError("endpoint cannot be None or empty...")

        if not extension:
            raise ValueError("extension cannot be None or empty...")

        uri = "{}/{}/{}".format(self.__uri, endpoint, extension)

        return uri

    def read_notebook(self, path: str, format: str = "SOURCE", direct: bool = True) -> str:

        if not path:
            raise ValueError("path cannot be None or empty...")

        endpoint = "workspace"
        extension = "export"

        uri = self.build_uri(endpoint, extension)

        body = {}
        
        body["path"] = path
        body["format"] = format
        body["direct_download"] = direct

        try:
            response = requests.get(uri, headers = self.__header, json = body)
            notebook = response.content.decode("ascii")
            return notebook
        except Exception as ex:
            raise ex

    def execute_notebook(self, path: str, existingClusterId: str = None, runName: str = None, timeOut: int = 3600) -> int:
        
        existingClusterId = existingClusterId if existingClusterId != None else self.__clusterId

        if not path:
            raise ValueError("path cannot be None or empty...")

        if not existingClusterId:
            raise ValueError("existing cluster id cannot be None or empty...")
        
        endpoint = "jobs"
        extension = "runs/submit"

        uri = self.build_uri(endpoint, extension)
        
        body = {}

        body["run_name"] = runName if runName != None else str(uuid.uuid4())
        body["existing_cluster_id"] = existingClusterId
        body["timeout_seconds"] = timeOut
        
        body["notebook_task"] = {}
        body["notebook_task"]["notebook_path"] = path

        try:
            response = requests.post(uri, headers = self.__header, json = body)
            runId = json.loads(response.content)["run_id"]
            return runId
        except Exception as ex:
            raise ex

    def get_run_state(self, runId: str) -> str:

        if not runId:
            raise ValueError("runId cannot be None or empty...")
        
        endpoint = "jobs"
        extension = "runs/get-output"

        uri = self.build_uri(endpoint, extension)
        
        body = {}

        body["run_id"] = runId

        try:
            response = requests.post(uri, headers = self.__header, json = body)
            # this might be limited to notebooks only, need to accomodate jobs and other executable structures if needed
            state = json.loads(response.content)["notebook_output"]["result"] 
            return state
        except Exception as ex:
            raise ex

    def get_run_uri(self, runId: str) -> str:

        if not runId:
            raise ValueError("run id cannot be None or empty...")

        endpoint = "jobs"
        extension = "runs/get"

        uri = self.build_uri(endpoint, extension)

        body = {}

        body["run_id"] = runId

        try:
            response = requests.get(uri, headers = self.__header, json = body)
            runUri = json.loads(response)["run_page_url"]
            return runUri
        except Exception as ex:
            raise ex

    def get_run_execution_time(self, runId: str) -> int:

        if not runId:
            raise ValueError("run id cannot be None or empty...")

        endpoint = "jobs"
        extension = "runs/get"

        uri = self.build_uri(endpoint, extension)

        body = {}
        body["run_id"] = runId

        try:
            response = requests.get(uri, headers = self.__header, json = body)
            runUri = json.loads(response)["execution_duration"]
            return runUri
        except Exception as ex:
            raise ex

    def get_notebook_details(self, runId: str) -> {}:

        if not runId:
            raise ValueError("run id cannot be None or empty...")

        endpoint = "jobs"
        extension = "runs/get"

        uri = self.build_uri(endpoint, extension)

        body = {}
        body["run_id"] = runId

        try:
            response = requests.get(uri, headers = self.__header, json = body)
            notebookDetails = json.loads(response)
            return notebookDetails
        except Exception as ex:
            raise ex

    def get_cluster_state(self, clusterId: str) -> str:

        clusterId = clusterId if clusterId != None else self.__clusterId

        if not clusterId:
            raise ValueError("clusterId cannot be None or empty...")
        
        endpoint = "clusters"
        extension = "get"

        uri = self.build_uri(endpoint, extension)
        
        body = {}

        body["cluster_id"] = runId

        try:
            response = requests.post(uri, headers = self.__header, json = body)
            state = json.loads(response.content)["state"] # need a wrapper class for state, enum, or const
            return state
        except Exception as ex:
            raise ex

    def start_cluster(self, clusterId: str = None) -> bool:

        clusterId = clusterId if clusterId != None else self.__clusterId

        if not clusterId:
            raise ValueError("cluster id cannot be None or empty...")

        state = self.get_cluster_state(clusterId)

        if state == "ERROR":
            raise Exception("cluster is in a state of error, please check cluster health with your admin...")

        if state == "TERMINATING":
            raise Exception("cluster is currently shutting down, cannot start cluster...")

        if state in ["RUNNING", "RESIZING", "RESTARTING"]:
            return True

        endpoint = "clusters"
        extension = "start"

        uri = self.build_uri(endpoint, extension)

        body = {}

        body["cluster_id"] = clusterId

        try:
            response = requets.post(uri, headers = self.__header, json = body)
            
            state = self.get_cluster_state(clusterId)

            while state == "PENDING":
                time.sleep(1)
                state = self.get_cluster_state(clusterId)

            if state == "Error":
                return False
            else:
                return True

        except Exception as ex:
            raise ex

    def terminate_cluster() -> bool:
        raise NotImplementedError("reserved by @phbennet")

    def create_cluster() -> bool:
        raise NotImplementedError("reserved by @phbennet")

    def create_notebook() -> bool:
        raise NotImplementedError("reserved by @phbennet")

    #endregion
