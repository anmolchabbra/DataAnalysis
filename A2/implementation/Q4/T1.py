from threading import Thread
import pandas as pd
import time

global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'

N0_OF_TOTAL_ROWS = 6311871
def findDates(readingItem: list):
    df = pd.read_csv(dataset, nrows=readingItem[0], skiprows=readingItem[1], header=None, low_memory=False)
    df = df.loc[pd.isna(df[7])]
    df = df.iloc[:, 0]
    flag = df.empty
    if not flag:
        flag = df.empty
        if not flag:
            dictNew = df.to_dict()
            for key, val in dictNew.items():
                result.append(val)

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


def printDates():
    res = pd.array(result)
    unique_res = pd.unique(res)
    #print("Length", len(unique_res))
    for date in unique_res:
        print(date)



def Thread_function(num_of_threads, readinginfo: list):
    thread_handle = []
    for j in range(0, num_of_threads):
        t = Thread((findDates(readinginfo[j])))
        thread_handle.append(t)

    for t in thread_handle:
        t.start()

    for j in range(0, num_of_threads):
        thread_handle[j].join()


if __name__ == '__main__':
    num_of_threads = int(input("Enter no of threads: "))
    readinginfo = []
    start = time.time()
    readinginfo = distribute_chunks(num_of_threads)
    result = []
    print('Processing...')
    Thread_function(num_of_threads, readinginfo)
    print("\n Dates for which departure time is not recorded or missing: ")
    printDates()
    print(f'time taken with {num_of_threads} threads (Multithreading execution): {round(time.time() - start, 2)} second(s)')
