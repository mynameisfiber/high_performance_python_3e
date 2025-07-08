from dataclasses import dataclass
from datetime import datetime
from itertools import count, filterfalse, groupby, islice
from operator import attrgetter
from random import normalvariate, randint

from scipy.stats import normaltest


@dataclass
class Datum:
    date: datetime
    value: float


def read_data(filename):
    with open(filename) as fd:
        for line in fd:
            data = line.strip().split(",")
            timestamp, value = map(int, data)
            yield Datum(datetime.fromtimestamp(timestamp), value)


def read_fake_data(filename):
    for timestamp in count():
        #  We insert an anomalous data point approximately once a week
        if randint(0, 7 * 60 * 60 * 24 - 1) == 1:
            value = 100
        else:
            value = normalvariate(0, 1)
        yield Datum(datetime.fromtimestamp(timestamp), value)


def groupby_day(iterable):
    key = lambda row: row.date.day
    for day, data_group in groupby(iterable, key):
        yield list(data_group)


def is_normal(data, threshold=1e-3):
    values = map(attrgetter("value"), data)
    _, p_value = normaltest(tuple(values))
    if p_value < threshold:
        return False
    return True


def filter_anomalous_groups(data):
    yield from filterfalse(is_normal, data)


def filter_anomalous_data(data):
    data_group = groupby_day(data)
    yield from filter_anomalous_groups(data_group)


if __name__ == "__main__":
    data = read_fake_data("fake_filename")
    anomaly_generator = filter_anomalous_data(data)
    first_five_anomalies = islice(anomaly_generator, 5)

    for data_anomaly in first_five_anomalies:
        start_date = data_anomaly[0].date
        end_date = data_anomaly[-1].date
        print(f"Anomaly from {start_date} - {end_date}")
