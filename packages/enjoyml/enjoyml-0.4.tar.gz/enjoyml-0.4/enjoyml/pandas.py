"""
Helper function which are used with pandas.
"""

import numpy as np
import pandas as pd
from typing import Any


def get_first_value_of_series(series: pd.Series) -> Any:
    """
    Returns first value of series

    TODO: how to remove any from type-hint for returned value
    :param series: row in pd.DataFrame
    :return: first value of series
    """

    return series.values[0]


def join_series_by_space(series: pd.Series) -> str:
    """
    Join series by space

    :param series: row in pd.DataFrame
    :return: joined pd.Series
    """

    # TODO прочекать или индекст не попадает в join
    return ' '.join(series.astype(str))


def join_columns_by_space(data_frame: pd.DataFrame) -> np.ndarray:
    """
    Join dataframe columns by space

    :param data_frame: pd.DataFrame
    :return: np.ndarray where each value is dataframe row joined by space
    """

    # TODO прочекать или индекст не попадает в join
    return data_frame.apply(lambda row: ' '.join(row.astype(np.str)), axis=1).values
