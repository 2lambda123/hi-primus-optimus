from optimus.tests.base import TestBase


class TestCSVPandas(TestBase):

    def test_csv(self):
        df = self.load_dataframe("examples/data/foo.csv")
        self.assertEqual(df.rows.count(), 19)
        self.assertEqual(df.cols.names(), ["id","firstName","lastName","billingId","product","price","birth","dummyCol"])

    def test_csv_13rows(self):
        df = self.load_dataframe("examples/data/foo.csv", n_rows=13)
        self.assertEqual(df.rows.count(), 13)
        self.assertEqual(df.cols.names(), ["id","firstName","lastName","billingId","product","price","birth","dummyCol"])        

    def test_csv_50rows(self):
        df = self.load_dataframe("examples/data/foo.csv", n_rows=50)
        self.assertLess(df.rows.count(), 50)
        self.assertEqual(df.cols.names(), ["id","firstName","lastName","billingId","product","price","birth","dummyCol"])        

class TestCSVDask(TestCSVPandas):
    config = {'engine': 'dask', 'n_partitions': 1}


class TestCSVPartitionDask(TestCSVPandas):
    config = {'engine': 'dask', 'n_partitions': 2}


try:
    import cudf # pyright: reportMissingImports=false
except:
    pass
else:
    class TestCSVCUDF(TestCSVPandas):
        config = {'engine': 'cudf'}


try:
    import dask_cudf # pyright: reportMissingImports=false
except:
    pass
else:
    class TestCSVDC(TestCSVPandas):
        config = {'engine': 'dask_cudf', 'n_partitions': 1}


try:
    import dask_cudf # pyright: reportMissingImports=false
except:
    pass
else:
    class TestCSVPartitionDC(TestCSVPandas):
        config = {'engine': 'dask_cudf', 'n_partitions': 2}


class TestCSVSpark(TestCSVPandas):
    config = {'engine': 'spark'}


class TestCSVVaex(TestCSVPandas):
    config = {'engine': 'vaex'}