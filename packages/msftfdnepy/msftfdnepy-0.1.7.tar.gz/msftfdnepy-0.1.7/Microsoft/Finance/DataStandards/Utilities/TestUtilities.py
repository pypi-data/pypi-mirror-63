from pyspark.sql.types import ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType, StringType
from re import search

class TestUtilities(object):

    #region Static Methods

    @staticmethod
    def check_pascal_case(s: str) -> bool:

        if not s:
            raise ValueError("s cannot be None or empty...")

        pascalPattern = r"^[A-Z][a-z]+(?:[A-Z][a-z]+)*$"
        searchResult = search(pascalPattern, s)
    
        if searchResult:
            return True
        else:
            return False

    @staticmethod
    def check_dimension_key_name(columnName: str) -> bool:

        if not columnName:
            raise ValueError("column name cannot be None or empty...")

        dimensionPrefix = "DIM_"
        dimensionSuffix = "Id"
    
        prefix = columnName[:4]
        suffix = columnName[-2:]

        return (prefix == dimensionPrefix and suffix == dimensionSuffix)

    @staticmethod
    def check_dimension_key_type(columnType: type) -> bool:

        if not columnType:
            raise ValueError("column type cannot be None...")
    
        dimensionType = IntegerType()

        return columnType == dimensionType

    @staticmethod
    def check_dimension_key_name_and_type(columnName: str, columnType: type) -> bool:

        if not columnName:
            raise ValueError("column name cannot be None or empty...")

        if not columnType:
            raise ValueError("column type cannot be None...")

        nameWellFormed = TestUtilities.check_dimension_key_name(columnName)
        tyepWellFormed = TestUtilities.check_dimension_key_type(columnType)

        return (nameWellFormed and tyepWellFormed)

    @staticmethod
    def check_flag_name(columnName: str) -> bool:

        if not columnName:
            raise ValueError("column name cannot be None or empty...")

        flagSuffix = "Flag"

        suffix = columnName[-4:]

        return suffix == flagSuffix

    @staticmethod
    def check_bad_flag_name(columnName: str) -> bool:

        if not columnName:
            raise ValueError("column name cannot be None or empty...")

        badFlagSuffix = "flag"

        suffix = columnName[-4:]

        return badFlagSuffix == suffix

    @staticmethod
    def check_flag_values(distinctColumnValues: [str]) -> bool:

        if not distinctColumnValues:
            raise ValueError("column values cannot be None or empty...")
    
        flagValues = set("Yes", "No", "Unknown", "N/A")

        for value in distinctColumnValues:
            if value not in flagValues:
                return False
    
        return True

    @staticmethod
    def check_flag_type(columnType: type) -> bool:

        if not columnType:
            raise ValueError("column type cannot be None...")

        flagType = StringType()

        return columnType == flagType

    @staticmethod
    def check_fact_type(columnType: type) -> bool:

        if not columnType:
            raise ValueError("column type cannot be None...")

        factTypes = set(ShortType(), IntegerType(), LongType(), FloatType(), DoubleType(), DecimalType())

        return (columnType in factTypes)

    #endregion