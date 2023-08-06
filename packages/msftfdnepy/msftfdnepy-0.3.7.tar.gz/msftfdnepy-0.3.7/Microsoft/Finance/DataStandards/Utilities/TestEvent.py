from datetime import datetime, timedelta
from json import dumps
from typing import Any
from uuid import uuid1

class TestEvent(object):

    #region Constructor

    def __init__(self, testName: str):
        self.__testName = testName
        self.__notes = {}
        self.__start = None
        self.__end = None
        self.__duration = None

    #endregion

    #region Overloads
    
    def __str__(self) -> str:

        # we'd prefer to use dumps(self.__dict__) but pyspark types are not json serializable

        d = {}

        d["test_name"] = self.TestName
        d["start"] = str(self.Start)
        d["end"] = str(self.End)
        d["duration"] = str(self.EventDurationSeconds)
        d["notes"] = {}

        for key in self.Notes.keys():
            
            val = self.Notes[key]

            if type(val) == list: #maybe expand to other types of enumerables like set
                d["notes"][key] = [str(e) for e in val]
            else:
                d["notes"][key] = str(val)

        s = dumps(d)

        return s
    
    #endregion
    
    #region Properties

    @property
    def TestName(self) -> str:
        return self.__testName

    @property
    def Notes(self) -> {}:
        return self.__notes

    @property
    def Start(self) -> datetime:
        return self.__start

    @property
    def End(self) -> datetime:
        return self.__end

    @property
    def EventDurationSeconds(self) -> float:
        if not self.__start or self.__end:
            return 0.0
        else:
            if not self.__duration:
                self.__duration = self.__end - self.__start
            return self.__duration.total_seconds()

    #endregion

    #region Class Methods

    def start(self) -> None:
        self.__start = datetime.now()
   
    def end(self) -> None:
        self.__end = datetime.now()

    def add_note(self, key: str, val: Any) -> None:

        if not key:
            raise ValueError("key cannot be None or empty...")

        if key in self.__notes.keys():
            key = "{}-{}".format(key, uuid1())

        self.__notes[key] = val

    #endregion