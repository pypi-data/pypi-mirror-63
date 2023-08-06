from Microsoft.Finance.Common.Utilities import Utilities
from Microsoft.Finance.Common.Spark import Spark
from Microsoft.Finance.DataStandards.Utilities.TestEvent import TestEvent
from Microsoft.Finance.DataStandards.Utilities.TestUtilities import TestUtilities

import unittest

class DimensionTestCase(unittest.TestCase):

    #region Constructor

    def __init__(self, sparkUtility: Spark, fieldInfo: {(str, type)}, databaseName: str, tableName: str, tableCount: int, customEvents: [TestEvent], methodName: str = "runTest") -> None:
        super(DimensionTestCase, self).__init__(methodName)
        self.__spark = sparkUtility
        self.__databaseName = databaseName
        self.__tableName = tableName
        self.__tableCount = tableCount
        self.__customEvents = customEvents
        self.__fieldInfo = fieldInfo

    #endregion

    #region Class Methods

    def test_primary_key_unique_values(self) -> None:

        '''
        desc
            Conventions for dimension tables
                g. Always check to make sure that there are no duplicates in Id column of dimension
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "key-with-unique-values"
        eventCode2 = "key-without-unique-values"
        eventCode3 = "non-key-columns"

        eventResults1 = []
        eventResults2 = []
        eventResults3 = []

        event.start()

        for columnName, columnType in self.__fieldInfo:
            if TestUtilities.check_dimension_key_name_and_type(columnName, columnType):
                keyValueCount = self.__spark.count_distinct_column_values(self.__databaseName, self.__tableName, columnName)
                if keyValueCount == tableCount:
                    eventResults1.append((columnName, columnType))
                else:
                    eventResults2.append((columnName, columnType))
            else:
                eventResults3.append((columnName, columnType))
        
        event.end()

        event.add_note(eventCode1, eventResults1)
        event.add_note(eventCode2, eventResults2)
        event.add_note(eventCode3, eventResults3)

        self.__customEvents.append(event)

        with self.subTest():
            self.assertEqual(len(eventResults1), 1)
        
        with self.subTest():
            self.assertEqual(len(eventResults2), 0)
    
    def test_primary_key(self) -> None:
        
        '''
        desc
            Conventions for dimension tables
                c. Unique column of table should be named as DIM_DimensionNameId and should always be of INT or BIGINT datatype
                d. Only the unique column of dimension should have “DIM” in name
        '''
        
        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "key-column"
        eventCode2 = "key-bad-type"
        eventCode3 = "non-key-columns"

        eventResults1 = []
        eventResults2 = []
        eventResults3 = []

        event.start()

        for columnName, columnType in self.__fieldInfo:
            if TestUtilities.check_dimension_key_name(columnName):
                if TestUtilities.check_dimension_key_type(columnType):
                    eventResults1.append((columnName, columnType))
                else:
                    eventResults2.append((columnName, columnType))
            else:
                eventResults3.append((columnName, columnType))
        
        event.end()
        
        event.add_note(eventCode1, eventResults1)
        event.add_note(eventCode2, eventResults2)
        event.add_note(eventCode3, eventResults3)

        self.__customEvents.append(event)

        with self.subTest():
            self.assertEqual(len(eventResults1), 1)
        
        with self.subTest():
            self.assertEqual(len(eventResults2), 0)
        
        with self.subTest():
            self.assertGreater(len(eventResults3), 0)

    #endregion