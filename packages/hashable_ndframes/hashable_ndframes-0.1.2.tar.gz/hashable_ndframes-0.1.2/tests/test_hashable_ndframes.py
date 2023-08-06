from hypothesis import given
from pandas import DataFrame
from pandas import Series

from hashable_ndframes.hashable_ndframes import HashableDataFrame
from hashable_ndframes.hashable_ndframes import HashableSeries
from tests.test_strategies import dataframes
from tests.test_strategies import series


@given(series=series())
def test_hashable_series(series: Series) -> None:
    hashable = HashableSeries(series)
    assert isinstance(hashable, Series)
    assert isinstance(hash(hashable), int)

    # test constructors
    assert isinstance(hashable.iloc[:0], HashableSeries)
    assert isinstance(hashable.to_frame(), HashableDataFrame)


@given(df=dataframes())
def test_hashable_dataframes(df: DataFrame) -> None:
    hashable = HashableDataFrame(df)
    assert isinstance(hashable, DataFrame)
    assert isinstance(hash(hashable), int)

    # test constructors
    assert isinstance(hashable.iloc[:0, :], HashableDataFrame)
    assert isinstance(hashable.iloc[:, 0], HashableSeries)
