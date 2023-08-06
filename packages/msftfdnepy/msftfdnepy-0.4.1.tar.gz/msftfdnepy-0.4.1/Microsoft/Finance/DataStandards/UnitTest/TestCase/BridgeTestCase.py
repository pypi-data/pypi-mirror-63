from Microsoft.Finance.Common.Utilities import Utilities 
from Microsoft.Finance.DataStandards.Utilities.TestUtilities import TestUtilities
from Microsoft.Finance.DataStandards.Utilities.TestEvent import TestEvent

import unittest

class BridgeTestCase(unittest.TestCase):

    #region Constructor

    def __init__(self, fieldInfo: [(str, type)], customEvents: [TestEvent], methodName: str = "runTest"):
        super(BridgeTestCase, self).__init__(methodName)
        self.__fieldInfo = fieldInfo
        self.__customEvents = customEvents

    #endregion

    #region Class Methods

    def test_bridge_columns_well_formed(self):
        
        '''
        desc
            Conventions for Bridge tables
                c. Output table should only contain dimension Ids and in some cases, degenerate attributes. Degenerate attributes should be added only where it is needed
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "dimension-id-columns"
        eventCode2 = "degenerate-attributes"
        eventCode3 = "bad-columns"

        eventResults1 = []
        eventResults2 = []
        eventResults3 = []

        event.start()

        for columnName, columnType in self.__fieldInfo:
            if TestUtilities.check_dimension_key_name(columnName):
                if TestUtilities.check_dimension_key_type(columnType):
                    eventResults1.append((columnName, columnType))
                else:
                    eventResults3.append((columnName, columnType))
            else:
                eventResults2.append((columnName, columnType))
        
        event.end()

        event.add_note(eventCode1, eventResults1)
        event.add_note(eventCode2, eventResults2)
        event.add_note(eventCode3, eventResults3)

        self.__customEvents.append(event)

        with self.subTest():
            self.assertGreater(len(eventResults1), 0)
        
        with self.subTest():
            self.assertEquals(len(eventResults3), 0)

    #endregion