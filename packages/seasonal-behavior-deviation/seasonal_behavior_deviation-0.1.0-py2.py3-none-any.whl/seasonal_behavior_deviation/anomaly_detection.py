# -*- coding: utf-8 -*-
import logging

from seasonal_behavior_deviation import __version__

__author__ = "Jannik Frauendorf"
__copyright__ = "Jannik Frauendorf"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def detect_anomalies(df, season_length, window_size, timestamp_col_name="timestamp", value_col_name="value"):
    # save current index for later usages
    df.loc[:, 'previous_index'] = df.index

    # set index to running number
    df = df.reset_index()
    df.loc[:, 'season_step'] = df.index % season_length

    # create normal behavior vector
    normal_behavior = df.groupby('season_step').agg({value_col_name: "median"})
    normal_behavior = normal_behavior.rename(columns={value_col_name: "normal_behavior"})

    # join normal behavior with original data
    df = pd.merge(df, normal_behavior, how='inner', on='season_step')

    # the join operation removes the order of the rows => reset the ordering to the timestamp column
    # set index to "timestamp"
    df = df.set_index(timestamp_col_name, drop=False)

    # sort by index
    df = df.sort_index()

    # generate sliding window data frame over the normal behavior vector and the value vector
    normal_behavior_windows = create_sliding_windows(df.loc[:, 'normal_behavior'], window_size)
    series_behavior_windows = create_sliding_windows(df.loc[:, value_col_name], window_size)

    # compute the Euclidean Distance row-wise between the two data frames
    scores = pd.Series(np.linalg.norm(normal_behavior_windows.values - series_behavior_windows.values, axis=1))

    # move anomaly scores to center of window
    first_part = int((anomaly_detection_win_size - 1) / 2)
    second_part = anomaly_detection_win_size - 1 - first_part
    df.loc[:, 'score'] = np.concatenate((np.zeros(first_part), scores, np.zeros(second_part)))
    df = df.set_index('previous_index', drop=True)

    return df
