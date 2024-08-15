import time
import multiprocessing
import pandas as pd
from multiprocessing import Pool

global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'
N0_OF_TOTAL_ROWS = 6311871

def map_tasks(reading_info: list):
    df = pd.read_csv(dataset, nrows=reading_info[0], skiprows=reading_info[1], header=None, low_memory=False)
    # return df.iloc[:, :1].value_counts()
    df = df[(df.iloc[:, 34] == "Nashville, TN") & (df.iloc[:, 42] == "Chicago, IL")]
    df = df.iloc[:, 12]
    df = df.dropna()
    return df.to_list()

def reduce_task(result):
    ans = {}
    for i in range(0, len(result)):
        if (len(result[i]) > 0):
            tempDic = result[i].to_dict()
            for key, value in tempDic.items():
                if key in ans:
                    ans[key] = ans[key] + value
                else:
                    ans[key] = value
    return ans


def findAverage(result):
    sum = 0
    len = 0
    for value in result:
        for value1 in value:
            sum += value1
            len += 1

    mean = sum / len
    return mean


def compute_multiprocessing():
    def distribute_chunks(numberOfProcesses: int):
        start = 1
        reading_info = []
        n_rows = N0_OF_TOTAL_ROWS / numberOfProcesses
        # leftOver = N0_OF_TOTAL_ROWS % numberOfThreads
        for i in range(0, numberOfProcesses):
            if (i == numberOfProcesses - 1):
                reading_info.append([None, int(start)])
            else:
                reading_info.append([int(n_rows), int(start)])
                start += n_rows
        return reading_info

    print("Processing...")
    processes = multiprocessing.cpu_count()
    p = Pool(processes=processes)
    result = p.map(map_tasks, distribute_chunks(processes))
    print(result)
    #ans = reduce_task(result)
    print("\n Average time of flights from Nashville to Chicago: ", findAverage(result))
    p.close()
    p.join()

if __name__ == '__main__':
    compute_multiprocessing()
