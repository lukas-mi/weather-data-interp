from datetime import datetime
import sys
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np


def load_data(file_path):
    def extract_data(line):
        elements = line.strip().split(",")
        return int(elements[0]), float(elements[1])

    with open(file_path, "r") as f:
        lines = f.readlines()

    data_kind = lines[0].strip().split(",")[1]
    data = map(extract_data, lines[1:])
    timestamps, values = map(list, zip(*data))

    return data_kind, timestamps, values


def take(hours, values, every_n_hours):
    filtered = filter(lambda pair: pair[0] % every_n_hours == 0, zip(hours, values))
    return map(list, zip(*filtered))


def plot(x_label, y_label, hours, values, filtered_hours, filtered_values):
    cubic_splines = interp1d(filtered_hours, filtered_values, kind='cubic')
    linear = interp1d(filtered_hours, filtered_values, kind='linear')

    x_new = np.linspace(min(filtered_hours), max(filtered_hours), 10000)

    plt.plot(hours, values, '.b', filtered_hours, filtered_values, 'or', x_new, cubic_splines(x_new), '-g', x_new, linear(x_new), '--y')

    plt.xlabel(x_label)
    plt.xticks(np.arange(min(hours), max(hours), 1))
    plt.ylabel(y_label)

    plt.legend(['data', 'data used for interpolation', 'cubic', 'linear'], loc='best')
    plt.show()


def labels(data_kind, timestamps):
    start = datetime.fromtimestamp(timestamps[0])
    end = datetime.fromtimestamp(timestamps[-1])
    x_label = "hours (from {start} to {end})".format(start=start, end=end)
    y_label = data_kind

    return x_label, y_label


def main():
    args = sys.argv
    if len(args) != 3:
        raise ValueError("error: arguments missing. "
                         "Required arguments: data file path, every n hours to take for interpolation")
    file_path = args[1]
    every_n_hours = int(args[2])

    data_kind, timestamps, values = load_data(file_path)
    hours = list(range(0, len(timestamps)))

    filtered_hours, filtered_values = take(hours, values, every_n_hours)
    x_label, y_label = labels(data_kind, timestamps)

    plot(x_label, y_label, hours, values, filtered_hours, filtered_values)


if __name__ == '__main__':
    main()
