from Microsoft.Finance.Common.Spark import Spark
from Microsoft.Finance.Common.Utilities import Utilities
from Microsoft.Finance.DataStandards.Utilities.TestEvent import TestEvent
from Microsoft.Finance.DataStandards.Utilities.TestUtilities import TestUtilities
from pyspark.sql.dataframe import DataFrame

import unittest

class FactTestCase(unittest.TestCase):

    #region Constructor

    def __init__(self, sparkUtility: Spark, tableDataFrame: DataFrame, fieldInfo: {(str, type)}, linkedDimensionTables: [(str, str)], databaseName: str, tableName: str, tableCount: int, customEvents: [TestEvent], excludeFromAggregation: [str] = [], methodName: str = "runTest"):
        super(FactTestCase, self).__init__(methodName)
        self.__spark = sparkUtility
        self.__tableDataFrame = tableDataFrame
        self.__fieldInfo = fieldInfo
        self.__linkedDimensionTables = linkedDimensionTables
        self.__databaseName = databaseName
        self.__tableName = tableName
        self.__tableCount = tableCount
        self.__customEvents = customEvents
        self.__excludeFromAggregation = excludeFromAggregation

    #endregion

    #region Class Methods

    def test_aggregation_efficiency(self) -> None:
        
        '''
        desc
            Conventions for fact tables
                e. Fact columns should be aggregated wherever possible
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "fact-columns"
        eventCode2 = "group-by-columns"
        eventCode3 = "custom-query"
        eventCode4 = "custom-count"

        factColumns = []
        groupByColumns = []

        event.start()

        for columnName, columnType in self.__fieldInfo:
            if columnName in self.__excludeFromAggregation or not TestUtilities.check_fact_type(columnType):
                groupByColumns.append(columnName)
            else:
                factColumns.append(columnName)
        
        factColumnAggregations = ["sum({})".format(columnName) for columnName in factColumns]
        
        factColumnString = ", ".join(factColumnAggregations)
        groupByColumnString = ", ".join(groupByColumns)

        customQuery = "select {}, {} from {}.{} group by {}".format(groupByColumnString, factColumnString, self.__databaseName, self.__tableName, groupByColumnString)
        customCount = self.__spark.count_query(customQuery)

        event.end()

        event.add_note(eventCode1, factColumns)
        event.add_note(eventCode2, groupByColumns)
        event.add_note(eventCode3, customQuery)
        event.add_note(eventCode4, customCount)

        self.__customEvents.append(event)

        with self.subTest():
            self.assertLessEqual(self.__tableCount, customCount)

    def test_column_categories(self) -> None:
        
        '''
        desc
            Conventions for fact tables
                c. Output table should only contain dimension Ids, fact columns and in some cases, degenerate attributes. Degenerate attributes should be added only where it is needed
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "dimension-keys"
        eventcode2 = "degenerate-attributes"
        eventCode3 = "fact-columns"
        eventCode4 = "bad-columns"

        dimensionKeys = []
        degenerateAttributes = []
        facts = []
        badColumns = []

        event.start()

        for columnName, columnType in self.__fieldInfo:
            if TestUtilities.check_dimension_key_name(columnName):
                if TestUtilities.check_dimension_key_type(columnType):
                    dimensionKeys.append((columnName, columnType))
                else:
                    badColumns.append((columnName, columnType))
            elif TestUtilities.check_fact_type(columnType):
                facts.append((columnName, columnType))
            else:
                degenerateAttributes.append((columnName, columnType))

        event.end()

        event.add_note(eventCode1, dimensionKeys)
        event.add_note(eventCode2, degenerateAttributes)
        event.add_note(eventCode3, facts)
        event.add_note(eventCode4, badColumns)

        self.__customEvents.append(event)
        
        with self.subTest():
            self.assertEqual(len(badColumns), 0)
        
        with self.subTest():
            self.assertGreater(len(facts), 0)
        
        with self.subTest():
            self.assertGreater(len(dimensionKeys), 0)

    def test_column_order(self) -> None:
        
        '''
        desc
            Conventions for fact tables
                i. Column sequencing should have all dimension Id columns first, followed by degenerate attributes and facts at the end
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "out-of-order-columns"
        eventCode2 = "index-of-last-dimension-key"
        eventCode3 = "index-of-last-degerate-attribute"

        outOfOrderColumns = []
        indexOfLastDimension = -float("inf")
        indexOfLastDegenerateAttribute = -float("inf")

        event.start()

        N = len(self.__fieldInfo)

        for i in range(N):
            if i < N - 1:
                if TestUtilities.check_dimension_key_name_and_type(self.__fieldInfo[i][0], self.__fieldInfo[i][1]):
                    if not TestUtilities.check_dimension_key_name_and_type(self.__fieldInfo[i + 1][0], self.__fieldInfo[i + 1][1]):
                        indexOfLastDimension = i
                        break
        
        degenerateAttributeStart = indexOfLastDimension + 1 if indexOfLastDimension > -float("inf") else 0

        for i in range(degenerateAttributeStart, N):
            if i < N - 1:
                if not TestUtilities.check_fact_type(self.__fieldInfo[i][1]) and TestUtilities.check_fact_type(self.__fieldInfo[i + 1][1]):
                    indexOfLastDegenerateAttribute = i
                    break
        
        factStart = indexOfLastDegenerateAttribute + 1 if indexOfLastDegenerateAttribute > -float("inf") else degenerateAttributeStart

        if indexOfLastDimension > -float("inf"):
            for i in range(indexOfLastDimension + 1):
                columnName = self.__fieldInfo[i][0]
                columnType = self.__fieldInfo[i][1]
                if not TestUtilities.check_dimension_key_name_and_type(columnName, columnType):
                    outOfOrderColumns.append((columnName, columnType))
        
        if indexOfLastDegenerateAttribute > float("inf"):
            for i in range(degenerateAttributeStart, indexOfLastDegenerateAttribute + 1):
                columnName = self.__fieldInfo[i][0]
                columnType = self.__fieldInfo[i][0]
                if TestUtilities.check_dimension_key_name(columnName) or TestUtilities.check_dimension_key_type(columnName):
                    outOfOrderColumns.append((columnName, columnType))
        
        for i in range(factStart, N):
            columnName = self.__fieldInfo[i][0]
            columnType = self.__fieldInfo[i][1]
            if not TestUtilities.check_fact_type(columnType):
                outOfOrderColumns.append((columnName, columnType))

        event.end()

        event.add_note(eventCode1, outOfOrderColumns)
        event.add_note(eventCode2, indexOfLastDimension)
        event.add_note(eventCode3, indexOfLastDegenerateAttribute)

        self.__customEvents.append(event)
        
        self.assertEqual(len(outOfOrderColumns), 0)

    def test_dimension_id_value_not_null(self) -> None:
        
        '''
        desc
            Conventions for fact tables
                d. Dimension Id columns included in fact tables should adhere to following:
                    d.1) Dimension Id column in fact should not be NULL
        '''

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "dimension-keys-with-nulls"

        dimensionsWithNulls = []

        event.start()

        for columnName, columnType in self.__fieldInfo:
            if TestUtilities.check_dimension_key_name_and_type(columnName, columnType):

                uniqueValues = self.__spark.get_distinct_column_values_from_df(self.__tableDataFrame, columnName)

                for val in uniqueValues:
                    if val == None:
                        dimensionsWithNulls.append((columnName, columnType))
                        break
        event.end()

        event.add_note(eventCode1, dimensionsWithNulls)
        
        self.assertEqual(len(dimensionsWithNulls), 0)

    def test_dimension_id_values_in_dimension(self) -> None:
        
        '''
        desc
            Conventions for fact tables
                d. Dimension Id columns included in fact tables should adhere to following:
                    d.2) Values in dimension Id column of fact should be present in actual dimension
        '''

        if(self.__linkedDimensionTables == None or len(self.__linkedDimensionTables) == 0):
            self.skipTest("the set of linked dimensions cannot be empty or None to run this test...")

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "keys-with-bad-values"

        keysWithBadValues = []
        dimensionFieldInfo = {}

        event.start()

        dimensionKeys = [column[0] for column in self.__fieldInfo if TestUtilities.check_dimension_key_name_and_type(column[0], column[1])]

        for dimensionInfo in self.__linkedDimensionTables:
            dimensionDatabaseName = dimensionInfo[0]
            dimensionTableName = dimensionInfo[1]
            dimensionFieldInfo[(dimensionDatabaseName, dimensionTableName)] = self.__spark.get_field_info_table_or_view(dimensionDatabaseName, dimensionTableName)

        for key in dimensionKeys:
            for dimInfo, schema in dimensionFieldInfo.items():
                
                dimensionColumns = {column[0] for column in schema}
                
                if key in dimensionColumns:
                    
                    dimensionDatabaseName = dimInfo[0]
                    dimensionTableName = dimInfo[1]
                    
                    keyValues = self.__spark.get_distinct_column_values_from_df(self.__tableDataFrame, key)
                    dimensionKeyValues = self.__spark.get_distinct_column_values(self.__sparkSession, dimensionDatabaseName, dimensionTableName, key)
                    
                    diff = keyValues - dimensionKeyValues
                    
                    if diff:
                        keysWithBadValues.append((dimensionTableName, key, diff))
        
        event.end()

        event.add_note(eventCode1, keysWithBadValues)

        self.assertEqual(len(keysWithBadValues), 0)

    def test_key_column_name_in_dimension(self) -> None:
        
        '''
        desc
            Conventions for fact tables
                d. Dimension Id columns included in fact tables should adhere to following:
                    d.4) Name of Dimension Id column should match to the actual column name in dimension table except in cases where the fact table relates to same dimension using multiple columns. In such cases, the relevant name should be added before DimensionId. E.g. DIM_StartDateId, DIM_EndDateId
        '''

        if(self.__linkedDimensionTables == None or len(self.__linkedDimensionTables) == 0):
            self.skipTest("the set of linked dimensions cannot be empty or None to run this test...")

        event = TestEvent(Utilities.get_function_caller_name())

        eventCode1 = "keys-not-in-dimension"

        keysNotInDimension = []
        keysInDimensions = []
        dimensionFieldInfo = {}

        event.start()

        for dimensionInfo in self.__linkedDimensionTables:
            dimensionDatabaseName = dimensionInfo[0]
            dimensionTableName = dimensionInfo[1]
            dimensionFieldInfo[dimensionTableName] = self.__spark.get_field_info_table_or_view(dimensionDatabaseName, dimensionTableName)

        keyColumns = [column[0] for column in self.__fieldInfo if TestUtilities.check_dimension_key_name_and_type(column[0], column[1])]
        
        for columnName in keyColumns:
            inDimension = False
            for dimensionName, dimensionSchema in dimensionFieldInfo.items():
                dimensionColumns = {column[0] for column in dimensionSchema}
                if columnName in dimensionColumns:
                    inDimension = True
                    keysInDimensions.append((columnName, dimensionName))
                    break
            
            if not inDimension:
                keysNotInDimension.append((columnName))

        event.end()

        event.add_note(eventCode1, keysNotInDimension)
        
        with self.subTest():
            self.assertEquals(len(keysNotInDimension), 0)
        
        with self.subTest():
            self.assertGreater(len(keysInDimensions), 0)

    #endregion