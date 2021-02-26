from enum import Enum

from optimus.helpers.logger import logger


# Python to PySpark reference
#
# type(None): NullType,
# bool: BooleanType,
# int: LongType,
# float: DoubleType,
# str: StringType,
# bytearray: BinaryType,
# decimal.Decimal: DecimalType,
# datetime.date: DateType,
# datetime.datetime: TimestampType,
# datetime.time: TimestampType,
# Profiler


class Actions(Enum):
    """
    Actions that modify a columns/rows.
    """
    # COLUMNS
    PROFILER_DTYPE = "profiler_dtype"
    LOWER = "lower"
    UPPER = "upper"
    PROPER = "proper"
    PAD = "pad"
    TRIM = "trim"
    REVERSE = "reverse"
    REMOVE_ACCENTS = "remove"
    REMOVE_SPECIAL_CHARS = "remove"
    REMOVE_WHITE_SPACES = "remove"
    LEFT = "left"
    RIGHT = "right"
    MID = "mid"
    REPLACE = "replace"
    REPLACE_REGEX = "replace"
    FILL_NA = "fill_na"
    CAST = "cast"
    IS_NA = "is_na"
    Z_SCORE = "z_score"
    NEST = "nest"
    UNNEST = "unnest"
    SET = "set"
    STRING_TO_INDEX = "string_to_index"
    DATE_FORMAT = "date_format"
    INDEX_TO_STRING = "index_to_string"
    MIN_MAX_SCALER = "min_max_scaler"
    MAX_ABS_SCALER = "max_abs_scaler"
    APPLY_COLS = "apply_cols"
    YEARS_BETWEEN = "apply_cols"
    IMPUTE = "impute"
    EXTRACT = "extract"
    ABS = "abs"
    MATH = "math"
    VARIANCE = "variance"
    SLICE = "slice"
    CLIP = "clip"
    DROP = "drop"
    KEEP = "keep"
    CUT = "cut"
    TO_FLOAT = "to_float"
    TO_INTEGER = "to_integer"
    TO_BOOLEAN = "to_boolean"
    TO_STRING = "to_string"
    YEAR = "years"
    APPEND = "append"
    PORT = "port"
    COPY = "copy"
    RENAME = "rename"

    # URL Example	http://search.somedb.com:8080/history?era=darkages
    # scheme	http
    # hostname	search.somedb.com
    # port	    8080
    # origin	http://search.somedb.com:8080
    # path	    /history
    # query	    ?era=darkages
    DOMAIN = "domain"
    DOMAIN_SCHEME = "domain_scheme"
    SUBDOMAIN = "subdomain"
    HOST = "host"
    DOMAIN_PARAMS = "domain_params"
    DOMAIN_PATH = "domain_path"

    EMAIL_DOMAIN = "email_domain"
    EMAIL_USER = "email_user"

    # ROWS
    SELECT_ROW = "select_row"
    DROP_ROW = "drop_row"
    BETWEEN_ROW = "between_drop"
    SORT_ROW = "sort_row"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Actions))


class ProfilerDataTypesQuality(Enum):
    MISMATCH = 0
    MISSING = 1
    MATCH = 2


class ProfilerDataTypes(Enum):
    INT = "int"
    DECIMAL = "decimal"
    STRING = "string"
    BOOLEAN = "boolean"
    DATE = "date"
    ARRAY = "array"
    OBJECT = "object"
    GENDER = "gender"
    IP = "ip"
    URL = "url"
    EMAIL = "email"
    CREDIT_CARD_NUMBER = "credit_card_number"
    ZIP_CODE = "zip_code"
    MISSING = "missing"
    CATEGORICAL = "categorical"
    PHONE_NUMBER = "phone_number"
    SOCIAL_SECURITY_NUMBER = "social_security_number"
    HTTP_CODE = "http_code"
    US_STATE = "us_state"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ProfilerDataTypes))

    # NULL = "null"
    # MISSING = "missing"

class Schemas(Enum):
    S3 = 's3://'
    GCS = 'gcs://'
    GC = 'gc://'
    HTTP = 'http://'
    HTTPS = 'https://'
    FTP = 'ftp://'
    FILE = 'file://'
    AZ = 'az://'
    ADL = 'adl://'
    ABFS = 'abfs://'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Schemas))


PROFILER_NUMERIC_DTYPES = [ProfilerDataTypes.INT.value, ProfilerDataTypes.DECIMAL.value]
PROFILER_STRING_DTYPES = [ProfilerDataTypes.STRING.value, ProfilerDataTypes.BOOLEAN.value,
                          ProfilerDataTypes.DATE.value, ProfilerDataTypes.ARRAY.value,
                          ProfilerDataTypes.OBJECT.value, ProfilerDataTypes.GENDER.value,
                          ProfilerDataTypes.IP.value, ProfilerDataTypes.URL.value,
                          ProfilerDataTypes.EMAIL.value, ProfilerDataTypes.CREDIT_CARD_NUMBER.value,
                          ProfilerDataTypes.ZIP_CODE.value, ProfilerDataTypes.PHONE_NUMBER,
                          ProfilerDataTypes.SOCIAL_SECURITY_NUMBER.value,
                          ProfilerDataTypes.HTTP_CODE.value, ProfilerDataTypes.US_STATE.value]

# Strings and Function Messages
JUST_CHECKING = "Just check that all necessary environments vars are present..."
STARTING_OPTIMUS = "Transform and Roll out..."

SUCCESS = "Optimus successfully imported. Have fun :)."

CONFIDENCE_LEVEL_CONSTANT = [50, .67], [68, .99], [90, 1.64], [95, 1.96], [99, 2.57]


def print_check_point_config(filesystem):
    logger.print(
        "Setting checkpoint folder %s. If you are in a cluster initialize Optimus with master='your_ip' as param",
        filesystem)


# For Google Colab
JAVA_PATH_COLAB = "/usr/lib/jvm/java-8-openjdk-amd64"
RELATIVE_ERROR = 10000

# Buffer size in rows
BUFFER_SIZE = 500000
