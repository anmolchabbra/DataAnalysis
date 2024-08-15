import time
import multiprocessing
import pandas as pd
from multiprocessing import Pool

global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'
N0_OF_TOTAL_ROWS = 6311871

def map_tasks(reading_info: list):
    df = pd.read_csv(dataset, nrows=reading_info[0], skiprows=reading_info[1], header=None, low_memory=False)
    df = df.loc[pd.isna(df[7])]
    df = df.iloc[:, 0]
    return df

def reduce_task(result):
    ans = []
    for i in range(0, len(result)):
        if (len(result[i]) > 0):
            ans.append(result[i].to_list())
    return ans

def printDates(result):
    total = 0
    alreadyAdded = []
    for item in result:
        res = pd.array(item)
        unique_res = pd.unique(res)
        for date in unique_res:
            if date not in alreadyAdded:
                total += 1
                print(date)
                alreadyAdded.append(date)


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
    #for analysis testing
    #processes = 4
    p = Pool(processes=processes)
    start = time.time()
    result = p.map(map_tasks, distribute_chunks(processes))
    #print(result)
    ans = reduce_task(result)
    #print(ans)
    print("\n Dates for which departure time is not recorded or missing: ")
    printDates(ans)
    p.close()
    p.join()
    print(f'time taken with {processes} processes (multiprocessing execution): {round(time.time() - start, 2)} second(s)')


if __name__ == '__main__':
    compute_multiprocessing()
