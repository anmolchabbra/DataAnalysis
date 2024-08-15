from threading import Thread
import pandas as pd
import math
import numpy as np
import time
from tqdm import tqdm

global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'
N0_OF_TOTAL_ROWS = 6311871

def findMostCanceledFlight(readingItem: list):
    df = pd.read_csv(dataset, nrows=readingItem[0], skiprows=readingItem[1], header=None, low_memory=False)
    # return df.iloc[:, :1].value_counts()
    df = df[(df.iloc[:, 0] >= "2021-09-01") & (df.iloc[:, 0] <= "2021-09-31")]
    df = df[df.iloc[:, 4] == True]
    df = df.iloc[:, [0, 1, 4]]
    df = pd.DataFrame(df.iloc[:, 1].value_counts())
    flag = df.empty
    if not flag:
        dictNew = df.to_dict(orient="dict")
        for key, val in dictNew.items():
            for key2, val2 in dictNew[key].items():
                if key2 in result:
                    result[key2] += val2
                else:
                    result[key2] = val2

'''Distrubute Chunks on the basis of number of threads'''
def distribute_chunks(numberOfThreads: int):
    start = 1
    reading_info = []
    n_rows = N0_OF_TOTAL_ROWS / numberOfThreads
    #leftOver = N0_OF_TOTAL_ROWS % numberOfThreads
    for i in range(0, numberOfThreads):
        if (i == numberOfThreads - 1):
            reading_info.append([None, int(start)])
        else:
            reading_info.append([int(n_rows), int(start)])
            start += n_rows
    return reading_info


def findMax():
    max = -1000
    name = ""
    for key, value in result.items():
        if result[key] > max:
            max = result[key]
            name = key
    return name


def Thread_function(num_of_threads, readinginfo: list):
    thread_handle = []
    for j in range(0, num_of_threads):
        t = Thread((findMostCanceledFlight(readinginfo[j])))
        thread_handle.append(t)

    for t in thread_handle:
        t.start()

    for j in range(0, num_of_threads):
        thread_handle[j].join()


if __name__ == '__main__':
    num_of_threads = int(input("Enter no of threads: "))
    readinginfo = []
    print('Processing...')
    readinginfo = distribute_chunks(num_of_threads)
    result = {}
    Thread_function(num_of_threads, readinginfo)
    print("\nAirlines with most cancelled flights in sep 2021: ", findMax())
