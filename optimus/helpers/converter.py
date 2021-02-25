from ast import literal_eval

import dateutil
from dask import dataframe as dd

# from optimus.helpers.check import is_cudf_dataframe, is_dask_dataframe, is_dask_cudf_dataframe, is_spark_dataframe, \
#     is_pandas_dataframe, is_cudf_series
from optimus.infer import is_dict, is_dict_of_one_element, is_list, is_list_of_one_element


def tuple_to_dict(value):
    """
    Convert tuple to dict
    :param value: tuple to be converted
    :return:
    """

    return dict((x, y) for x, y in value)


def format_dict(_dict, tidy=True):
    """
    This function format a dict. If the main dict or a deep dict has only on element
     {"col_name":{0.5: 200}} we get 200
    :param _dict: dict to be formatted
    :param tidy:
    :return:
    """

    if tidy is True:
        def _format_dict(_dict):

            if not is_dict(_dict):
                return _dict
            for k, v in _dict.items():
                # If the value is a dict
                if is_dict(v):
                    # and only have one value
                    if len(v) == 1:
                        _dict[k] = next(iter(v.values()))
                else:
                    if len(_dict) == 1:
                        _dict = v
            return _dict

        if is_list_of_one_element(_dict):
            _dict = _dict[0]
        elif is_dict_of_one_element(_dict):
            # if dict_depth(_dict) >4:
            _dict = next(iter(_dict.values()))

        # Some aggregation like min or max return a string column

        def repeat(f, n, _dict):
            if n == 1:  # note 1, not 0
                return f(_dict)
            else:
                return f(repeat(f, n - 1, _dict))  # call f with returned value

        # TODO: Maybe this can be done in a recursive way
        # We apply two passes to the dict so we can process internals dicts and the superiors ones
        return repeat(_format_dict, 2, _dict)
    else:
        # Return the dict from a list
        if is_list(_dict):
            return _dict[0]
        else:
            return _dict

#
# def str_to_boolean(value):
#     """
#     Check if a str can be converted to boolean
#     :param value:
#     :return:
#     """
#     value = value.lower()
#     if value == "true" or value == "false":
#         return True
#
#
# def str_to_date(value):
#     try:
#         dateutil.parser.parse(value)
#         return True
#     except (ValueError, OverflowError):
#         pass
#
#
# def str_to_array(value):
#     """
#     Check if value can be parsed to a tuple or and array.
#     Because Spark can handle tuples we will try to transform tuples to arrays
#     :param value:
#     :return:
#     """
#     try:
#         if isinstance(literal_eval((value.encode('ascii', 'ignore')).decode("utf-8")), (list, tuple)):
#             return True
#     except (ValueError, SyntaxError,):
#         pass
#

# Functions to convert dataframe between engines

def any_dataframe_to_pandas(df):
    # print(type(df))
    if is_pandas_dataframe(df):
        result = df
    elif is_spark_dataframe(df):
        result = spark_to_pandas(df)
    elif is_dask_dataframe(df):
        result = dask_dataframe_to_pandas(df)
    elif is_cudf_dataframe(df) or is_cudf_series(df):
        result = cudf_to_pandas(df)
    elif is_dask_cudf_dataframe(df):
        result = dask_cudf_to_pandas(df)

    return result

#
# def cudf_series_to_pandas(serie):
#     return serie.to_pandas()
#
#
# def dask_dataframe_to_dask_cudf(df):
#     import cudf
#     return df.map_partitions(cudf.DataFrame.from_pandas)
#
#
# # To cudf
# def dask_dataframe_to_cudf(df):
#     return pandas_to_cudf(dask_dataframe_to_pandas(df))
#
#
# def dask_cudf_to_cudf(df):
#     return df.compute()


# To Pandas
def spark_to_pandas(df):
    return df.toPandas()


def dask_cudf_to_pandas(df):
    return df.map_partitions(lambda df: df.to_pandas())


def dask_dataframe_to_pandas(df):
    return df.compute()


def cudf_to_pandas(df):
    return df.to_pandas()

#
# def cudf_to_dask_cudf(df, n_partitions=1):
#     import dask_cudf
#     return dask_cudf.from_cudf(df, npartitions=1)
#
#
# def cudf_to_cupy_arr(df):
#     import cupy as cp
#     return cp.fromDlpack(df.to_dlpack())
#
#
# def pandas_to_cudf(df):
#     import cudf
#     return cudf.from_pandas(df)


def pandas_to_dask_dataframe(pdf, n_partitions=1):
    return dd.from_pandas(pdf, npartitions=n_partitions)

def pandas_to_dask_cudf_dataframe(pdf, n_partitions=1):
    import cudf
    import dask_cudf
    # Seems that from_cudf also accepts pandas
    cdf = cudf.DataFrame.from_pandas(pdf)
    return dask_cudf.from_cudf(cdf, npartitions=n_partitions)

