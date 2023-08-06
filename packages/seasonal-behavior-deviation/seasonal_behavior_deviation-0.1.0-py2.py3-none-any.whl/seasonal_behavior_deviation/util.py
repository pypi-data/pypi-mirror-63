# -*- coding: utf-8 -*-
import logging
from skimage.util.shape import view_as_windows
import numpy as np
import pandas as pd

from seasonal_behavior_deviation import __version__

__author__ = "Jannik Frauendorf"
__copyright__ = "Jannik Frauendorf"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def remove_duplicate_rows(df, timestamp_col_name='timestamp', value_col_name='value'):
    """
    Remove duplicates of the timestamp-column-combination in the given df.
    """
    return df.drop_duplicates(subset=[timestamp_col_name, value_col_name], keep='first')


def create_sliding_windows(series, window_size):
    """
    Computes the result of a sliding window over the given vector with the given window size.
    Each row represents the content of the sliding window at each position.
    :param series: a pandas Series
    :param window_size: a integer specifying the width of the sliding window.
    """
    vector = np.array(series)
    return pd.DataFrame(view_as_windows(vector, window_size))
