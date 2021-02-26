import re
from abc import abstractmethod, ABC

import numpy as np

from optimus.helpers.core import val_to_list
from optimus.infer import regex_full_url


class Functions(ABC):
    @staticmethod
    def delayed(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def _to_float(series):
        pass

    def to_integer(self, series):
        pass

    def to_string(self, series):
        pass

    # Aggregation
    def min(self, series):
        return self._to_float(series).min()

    def max(self, series):
        return self._to_float(series).max()

    def mean(self, series):

        return self._to_float(series).mean()

    def mode(self, series):
        return self._to_float(series).mode().to_dict()

    def std(self, series):
        return self._to_float(series).std()

    def sum(self, series):
        return self._to_float(series).sum()

    def cumsum(self, series):
        return self._to_float(series).cumsum()

    def cumprod(self, series):
        return self._to_float(series).cumprod()

    def cummax(self, series):
        return self._to_float(series).cummax()

    def cummin(self, series):
        return self._to_float(series).cummin()

    def var(self, series):
        return self._to_float(series).var()

    @staticmethod
    def count_uniques(series, estimate: bool = True, compute: bool = True):
        # series = self.series
        return self.to_string(series).nunique()

    @staticmethod
    def unique(series, *args):

        # print("args",args)
        # Cudf can not handle null so we fill it with non zero values.
        return self.to_string(series).unique()

    @staticmethod
    def count_na(series):
        return series.isna().sum()

        # return {"count_na": {col_name:  for col_name in columns}}
        # return np.count_nonzero(_df[_serie].isnull().values.ravel())
        # return cp.count_nonzero(_df[_serie].isnull().values.ravel())

    @staticmethod
    @abstractmethod
    def count_zeros(series, *args):
        pass

    @staticmethod
    @abstractmethod
    def kurtosis(series):
        pass

    @staticmethod
    @abstractmethod
    def skew(series):
        pass

    @staticmethod
    def mad(series, *args):
        error, more = args

        series = series._to_float()
        if series.isnull().any():
            mad_value = np.nan
            median_value = np.nan
        else:
            median_value = series.quantile(0.5)
            mad_value = {"mad": (series - median_value).abs().quantile(0.5)}

        # median_value = series.quantile(0.5)
        # # In all case all the values from the column
        # # are nan because can not be converted to number
        # if not np.isnan(median_value):
        #     mad_value = {"mad": (series - median_value).abs().quantile(0.5)}
        # else:
        #     mad_value = np.nan

        if more:
            mad_value.update({"median": median_value})
        return mad_value

    # TODO: dask seems more efficient triggering multiple .min() task, one for every column
    # cudf seems to be calculate faster in on pass using df.min()
    def range(self, series):
        series = series._to_float()
        return {"min": series.min(), "max": series.max()}

    def percentile(self, series, values, error):

        series = self._to_float(series)

        @self.delayed
        def to_dict(_result):
            ## In pandas if all values are none it return {} on dict
            # Dask raise an exception is all values in the series are np.nan
            if _result.isnull().all():
                return np.nan
            else:
                return _result.quantile(values).to_dict()

        return to_dict(series)

    # def radians(series):
    #     return series._to_float().radians()
    #
    # def degrees(series, *args):
    #     return call(series, method_name="degrees")

    ###########################

    @staticmethod
    @abstractmethod
    def clip(series, lower_bound, upper_bound):
        pass

    @staticmethod
    @abstractmethod
    def cut(series, bins):
        pass

    def abs(self, series):
        return self._to_float(series).abs()

    def exp(self, series):
        return self._to_float(series).exp()

    @staticmethod
    @abstractmethod
    def sqrt(series):
        pass

    def mod(self, series, other):
        return self._to_float(series).mod(other)

    def round(self, series, decimals):
        return self._to_float(series).round(decimals)

    def pow(self, series, exponent):
        return self._to_float(series).pow(exponent)

    def floor(self, series):
        return self._to_float(series).floor()

    # def trunc(self):
    #     series = self.series
    #     return series._to_float().truncate()

    @staticmethod
    @abstractmethod
    def radians(series):
        pass

    @staticmethod
    @abstractmethod
    def degrees(series):
        pass

    @staticmethod
    @abstractmethod
    def ln(series):
        pass

    @staticmethod
    @abstractmethod
    def log(series, base):
        pass

    @staticmethod
    @abstractmethod
    def ceil(series):
        pass

    @staticmethod
    @abstractmethod
    def sin(series):
        pass

    @staticmethod
    @abstractmethod
    def cos(series):
        pass

    @staticmethod
    @abstractmethod
    def tan(series):
        pass

    @staticmethod
    @abstractmethod
    def asin(series):
        pass

    @staticmethod
    @abstractmethod
    def acos(series):
        pass

    @staticmethod
    @abstractmethod
    def atan(series):
        pass

    @staticmethod
    @abstractmethod
    def sinh(series):
        pass

    @staticmethod
    @abstractmethod
    def cosh(series):
        pass

    @staticmethod
    @abstractmethod
    def tanh(series):
        pass

    @staticmethod
    @abstractmethod
    def asinh(series):
        pass

    @staticmethod
    @abstractmethod
    def acosh(series):
        pass

    @staticmethod
    @abstractmethod
    def atanh(series):
        pass

    # Strings
    def lower(self, series):
        return self.to_string(series).str.lower()

    @staticmethod
    def upper(series):
        return self.to_string(series).str.upper()

    @staticmethod
    def title(series):
        return self.to_string(series).str.title()

    @staticmethod
    def capitalize(series):
        return self.to_string(series).str.capitalize()

    @staticmethod
    def pad(series, width, side, fillchar=""):
        return self.to_string(series).str.pad(width, side, fillchar)

    @staticmethod
    def extract(series, regex):
        return self.to_string(series).str.extract(regex)

    @staticmethod
    def slice(series, start, stop, step):
        return self.to_string(series).str.slice(start, stop, step)

    @staticmethod
    def proper(series):
        return self.to_string(series).str.title()

    @staticmethod
    def trim(series):
        return self.to_string(series).str.strip()

    @staticmethod
    @abstractmethod
    def replace_chars(series, search, replace_by):
        pass

    @staticmethod
    def replace_words(series, search, replace_by):
        search = val_to_list(search)
        str_regex = (r'\b%s\b' % r'\b|\b'.join(map(re.escape, search)))
        return self.to_string(series).str.replace(str_regex, replace_by)

    @staticmethod
    def replace_full(series, search, replace_by):
        search = val_to_list(search)
        str_regex = (r'\b%s\b' % r'\b|\b'.join(map(re.escape, search)))
        return self.to_string(series).str.replace(str_regex, replace_by)

    @staticmethod
    def remove_white_spaces(series):
        return self.to_string(series).str.replace(" ", "")

    @staticmethod
    def len(series):
        return series.str.len()

    def to_datetime(self, series, format):
        pass

    def normalize_chars(self, series):
        pass

    @staticmethod
    def find(self, sub, start=0, end=None):
        series = self.series
        return self.to_string(series).str.find(sub, start, end)

    @staticmethod
    def rfind(series, sub, start=0, end=None):
        return self.to_string(series).str.rfind(sub, start, end)

    @staticmethod
    def left(series, position):
        return self.to_string(series).str[:position]

    @staticmethod
    def right(series, position):
        return self.to_string(series).str[-1 * position:]

    @staticmethod
    def mid(series, _start, _n):
        return self.to_string(series).str[_start:_n]

    @staticmethod
    def starts_with(series, pat):
        return self.to_string(series).str.startswith(pat)

    @staticmethod
    def ends_with(series, pat):
        return self.to_string(series).str.endswith(pat)

    @staticmethod
    def contains(series, pat):
        return self.to_string(series).str.contains(pat)

    @staticmethod
    def char(series, _n):
        return self.to_string(series).str[_n]

    @staticmethod
    def unicode(series):
        pass

    @staticmethod
    def exact(series, pat):
        return series == pat

    # dates
    def year(self, series, format):
        """
        :param series:
        :param format: "%Y-%m-%d HH:mm:ss"
        :return:
        """
        # return self.to_datetime(format=format).strftime('%Y').to_self().reset_index(drop=True)
        return self.to_datetime(series, format=format).dt.year

    @staticmethod
    def month(series, format):
        return series.to_datetime(format=format).dt.month

    @staticmethod
    def day(series, format):
        return series.to_datetime(format=format).dt.day

    @staticmethod
    def hour(series, format):
        return series.to_datetime(format=format).dt.hour

    @staticmethod
    def minute(series, format):
        return series.to_datetime(format=format).dt.minute

    @staticmethod
    def second(series, format):
        return series.to_datetime(format=format).dt.second

    @staticmethod
    def weekday(series, format):
        return series.to_datetime(format=format).dt.weekday

    @staticmethod
    @abstractmethod
    def date_format(self, current_format=None, output_format=None):
        pass

    @staticmethod
    @abstractmethod
    def years_between(self, date_format=None):
        pass

    def domain(self, series):
        return series.str.extract(regex_full_url)[5]

    def url_scheme(self, series):
        return series.str.extract(regex_full_url)[1]

    def url_params(self, series):
        return series.str.extract(regex_full_url)[9]

    def url_path(self, series):
        return series.str.extract(regex_full_url)[8]

    def port(self, series):
        return series.str.extract(regex_full_url)[6]

    def subdomain(self, series):
        return series.str.extract(regex_full_url)[4]

    def email_username(self, series):
        return series.str.split('@')[0][0]

    def email_domain(self, series):
        return series.str.split('@')[0][1]
