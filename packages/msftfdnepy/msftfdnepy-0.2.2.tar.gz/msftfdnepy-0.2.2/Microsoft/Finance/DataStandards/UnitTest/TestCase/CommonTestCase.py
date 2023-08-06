from Microsoft.Finance.Common.Spark import Spark
from Microsoft.Finance.Common.Utilities import Utilities 
from Microsoft.Finance.DataStandards.Utilities.TestUtilities import TestUtilities
from Microsoft.Finance.DataStandards.Utilities.TestEvent import TestEvent
from pyspark.sql.dataframe import DataFrame

import unittest

class CommonTestCase(unittest.TestCase):

    #region Constructor

    def __init__(self, tableDataFrame: DataFrame, fieldInfo: {(str, type)}, customEvents: [TestEvent], methodName: str = "runTest"):
        super(CommonTestCase, self).__init__(methodName)
        self.__tableDataFrame = tableDataFrame
        self.__fieldInfo = fieldInfo
        self.__customEvents = customEvents

    #endregion

    #region Class Methods

    def test_pascal_casing(self) -> None:

        '''
        desc
            Conventions for fact, dimension, staging, bridge tables
                *. Column names should use Pascal Casing and should not have spaces
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "pascal-case-columns"
        eventCode2 = "not-pascal-case-columns"
        eventCode3 = "dimension-keys"

        eventResults1 = []
        eventResults2 = []
        eventResults3 = []

        event.start()

        columnNames = [field[0] for field in self.__fieldInfo]

        for columnName in columnNames:
            if TestUtilities.check_dimension_key_name(columnName):
                eventResults3.append(columnName)
            else:
                if TestUtilities.check_pascal_case(columnName):
                    eventResults1.append(columnName)
                else:
                    eventResults2.append(columnName)
        
        event.end()

        event.add_note(eventCode1, eventResults1)
        event.add_note(eventCode2, eventResults2)
        event.add_note(eventCode3, eventResults3)

        self.__customEvents.append(event)

        with self.subTest():
            self.assertEquals(len(eventResults1), len(columnNames) - len(eventResults3))
        
        with self.subTest():
            self.assertEquals(len(eventResults2), 0)

    def test_flag_values(self) -> None:

        '''
        desc
            Conventions for Flags
                a. All the flag should be named as AbcFlag (examples: DynamicsFlag or CloudAddOnFlag)
                b. Possible values for Flags: Yes, No, Unknown, N/A
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "well-formed-flags"
        eventCode2 = "flag-with-bad-name"
        eventCode3 = "flags-with-bad-values"
        eventCode4 = "non-flag-columns"

        eventResults1 = []
        eventResults2 = []
        eventResults3 = []
        eventResults4 = []

        event.start()

        for columnName, columnType in self.__fieldInfo:
            if TestUtilities.check_flag_name(columnName):
                if not check_flag_type(columnType):
                    eventResults3.append((columnName, columnType))
                else:
                    flagValues = Spark.get_distinct_column_values_from_df(self.__tableDataFrame, columnName)
                    if check_flag_values(flagValues):
                        eventResults1.append((columnName, columnType))
                    else:
                        eventResults3.append((columnName, columnType))
            elif TestUtilities.check_bad_flag_name(columnName):
                eventResults2.append((columnName, columnType))
            else:
                eventResults4.append((columnName, columnType))
        
        event.end()

        event.add_note(eventCode1, eventResults1)
        event.add_note(eventCode2, eventResults2)
        event.add_note(eventCode3, eventResults3)
        event.add_note(eventCode4, eventResults4)

        self.__customEvents.append(event)

        with self.subTest():
            self.assertEqual(len(eventResults2), 0)
        
        with self.subTest():
            self.assertEqual(len(eventResults3), 0)

    #endregion