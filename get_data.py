from datetime import datetime
import math
import sys
import os
import requests

BASE_ENDPOINT = "https://api.darksky.net/forecast/{api_key}/{latitude},{longitude}?units=si&exclude=flags,daily"
DOC_ENDPOINT = "https://darksky.net/dev/docs#data-point"


def extract_data(hourly_data, key):
    def extract_data_h(hourly_data_point):
        return {'timestamp': hourly_data_point['time'], 'data': hourly_data_point[key]}

    return list(map(extract_data_h, hourly_data))


def save_csv(data, data_kind):
    ts = math.floor(datetime.now().timestamp())
    file_path = "data/{timestamp}_{data_kind}.csv".format(timestamp=ts, data_kind=data_kind)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "a+") as f:
        header = "timestamp,{data_kind}\n".format(data_kind=data_kind)
        f.write(header)

        for d in data:
            line = "{timestamp},{data}\n".format(timestamp=d['timestamp'], data=d['data'])
            f.write(line)


def main():
    args = sys.argv
    if len(args) != 5:
        raise ValueError("error: arguments missing. Required arguments: api key, latitude, longitude and data kind")

    api_key = args[1]
    latitude = float(args[2])
    longitude = float(args[3])
    data_kind = args[4]

    endpoint = BASE_ENDPOINT.format(api_key=api_key, latitude=latitude, longitude=longitude)
    print("querying {endpoint}".format(endpoint=endpoint))

    response = requests.get(endpoint)
    response.raise_for_status()

    hourly_data = response.json()['hourly']['data']

    try:
        extracted_data = extract_data(hourly_data, data_kind)
    except KeyError:
        print("error: hourly data point does not contain data for '{data_kind}', see documentation at {doc_endpoint}"
              .format(data_kind=data_kind, doc_endpoint=DOC_ENDPOINT))
        sys.exit(1)

    print("saving {data_kind} data to csv".format(data_kind=data_kind))
    save_csv(extracted_data, data_kind)


if __name__ == '__main__':
    main()
