import pandas as pd
from pandas._config import get_option
from pandas.io.formats import console
from io import StringIO

ANONIMIZED = False

series_orig_repr = pd.Series.__repr__

# pd.Series.__repr__ = lambda *args: "a"


class AnonimizedSeries:
    def __init__(self, data, key):
        self.data = pd.Series(data)
        self._key = key

    def __len__(self):
        return len(self.data)

    def value_counts(self):
        return pd.Series(self.data).value_counts()._values

    def head(self):
        return AnonimizedSeries(pd.Series.head(self.data), self._key)

    def tail(self):
        return AnonimizedSeries(pd.Series.tail(self.data), self._key)

    def __repr__(self):
        return repr(pd.Series([self._key] * len(self)))

    def __getattribute__(self, key):
        if key == "iloc":
            raise ValueError("Cannot iloc anonimized object")
        return super().__getattribute__(key)

    @property
    def str(self):
        return pd.Series(self.data).str


def series_anon_repr(x):
    return "<AnonimizedSeries>"


def anon(x):
    def ret_inner(y):
        return "*" * len(x)

    return ret_inner


def normal(y):
    return str(y).replace("\n", "\\n")


class Anonimizer(pd.DataFrame):
    anonimized = []

    def __getitem__(self, key):
        if isinstance(key, str) and ANONIMIZED and key in self.anonimized:
            return AnonimizedSeries(pd.DataFrame.__getitem__(self, key), key)
        return pd.DataFrame.__getitem__(self, key)

    def __repr__(self) -> str:
        global ANONIMIZED
        if not ANONIMIZED:
            return super().__repr__()
        """
        Return a string representation for a particular DataFrame.
        """
        buf = StringIO("")
        if self._info_repr():
            self.info(buf=buf)
            return buf.getvalue()
        max_rows = get_option("display.max_rows")
        min_rows = get_option("display.min_rows")
        max_cols = get_option("display.max_columns")
        max_colwidth = get_option("display.max_colwidth")
        show_dimensions = get_option("display.show_dimensions")
        if get_option("display.expand_frame_repr"):
            width, _ = console.get_console_size()
        else:
            width = None
        formatters = [(anon(x) if x in self.anonimized else normal) for x in self.columns]
        self.to_string(
            buf=buf,
            max_rows=max_rows,
            min_rows=min_rows,
            max_cols=max_cols,
            line_width=width,
            max_colwidth=max_colwidth,
            show_dimensions=show_dimensions,
            formatters=formatters,
        )
        return buf.getvalue()

    @classmethod
    def anonimize(cls):
        global ANONIMIZED
        ANONIMIZED = True

    @classmethod
    def reveal(cls):
        global ANONIMIZED
        ANONIMIZED = False
