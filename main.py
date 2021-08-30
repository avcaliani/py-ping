from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from random import choice
import pandas as pd

import subprocess
import re
import os

COMMAND = 'ping -t 1 8.8.8.8'
RESULT_PATTERN = r'.*time=(\d+\.?\d*)\sms'
DURATION = 60 * 60 * 4  # Seconds
SLEEP_TIME = 1 # Seconds
MAX_ACCEPTABLE_LATENCY = 70

ORANGE = '1;38;5;202'
RED = '1;31'
GREEN = '1;32'

def color(color_pattern, value):
    return f'\033[{color_pattern}m{value}\033[00m'

def ping():
    process = subprocess.Popen(COMMAND.split(), stdout=subprocess.PIPE, universal_newlines=True)
    stdout = process.stdout.readlines()
    for line in stdout:
        res = re.search(RESULT_PATTERN, line.strip(), re.IGNORECASE)
        if res:
            latency = float(res.group(1))
            return latency
    print(f'NOT FOUND: {line.strip()}')
    return -1



def add_result(date, latency):
    chart_color, shape, log_color = 'green', '.', GREEN
    if latency <= 0:
        chart_color, shape, log_color = 'red', 'X', RED
    if latency > MAX_ACCEPTABLE_LATENCY:
        chart_color, shape, log_color = 'orange', '^', ORANGE
    print(f'Time: {date.strftime("%Y-%m-%d %H:%M:%S")} | Latency: {color(log_color, latency)} ms')
    plt.scatter(x=date, y=latency, c=chart_color, marker=shape)
    plt.pause(SLEEP_TIME)


def main():
    started_at = datetime.now()
    ending = datetime.now() + timedelta(seconds=DURATION)
    records = []
    while datetime.now() < ending:
        rec = {'date': datetime.now(), 'latency': ping()}
        records.append(rec)
        add_result(**rec)
    
    df = pd.DataFrame(records)
    print(f'Min. Latency: {df["latency"].min()}')
    print(f'Max. Latency: {df["latency"].max()}')
    print(f'AVG. Latency: {df["latency"].mean()}')
    print(f'Duration: {df["date"].max() - df["date"].min()}')
    print('** END **')
    os.makedirs('data', exist_ok=True)
    df.to_csv(f'data/{started_at.strftime("%Y%m%d.%H%M%S")}.csv', index=False)
    plt.show()

if __name__ == '__main__':
    main()
