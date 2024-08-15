import time
import multiprocessing
import pandas as pd
from multiprocessing import Pool

global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'
N0_OF_TOTAL_ROWS = 6311871

def map_tasks(reading_info: list):
    df = pd.read_csv(dataset, nrows=reading_info[0], skiprows=reading_info[1], header=None)
    #return df.iloc[:, :1].value_counts()
    df = df[(df.iloc[:, 0] >= "2021-09-01") & (df.iloc[:, 0] <= "2021-09-31")]
    df = df[df.iloc[:, 4] == True]
    df = df.iloc[:, [0, 1, 4]]
    df = pd.DataFrame(df.iloc[:, 1].value_counts())
    return df


def reduce_task(result: list):
    ans = {}
    for i in range(0, len(result)):
        if (len(result[i]) > 0):
            tempDic = result[i].to_dict()
            for key, value in tempDic.items():
                for key1, value1 in value.items():
                    if key1 in ans:
                        ans[key1] = ans[key1] + value1
                    else:
                        ans[key1] = value1
    return ans


def findMax(result_dict):
    max = -1000
    name = ""
    for key, value in result_dict.items():
        if result_dict[key] > max:
            max = result_dict[key]
            name = key
    return name


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

   # print(distribute_rows(n_rows=200000, n_processes=multiprocessing.cpu_count()))
    print('Processing...')
    processes = multiprocessing.cpu_count()
    p = Pool(processes=processes)
    result = p.map(map_tasks, distribute_chunks(processes))
    ans = reduce_task(result)
    name = findMax(ans)
    print("\nAirlines with most cancelled flights in sep 2021: ", name)
    p.close()
    p.join()

if __name__ == '__main__':
    compute_multiprocessing()
