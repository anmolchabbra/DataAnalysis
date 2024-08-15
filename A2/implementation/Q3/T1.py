from threading import Thread
import pandas as pd


global dataset
dataset = '/./Combined_Flights_2021.csv'

N0_OF_TOTAL_ROWS = 6311871
def findAirtime(readingItem: list):
    df = pd.read_csv(dataset, nrows=readingItem[0], skiprows=readingItem[1], header=None, low_memory=False)
    # return df.iloc[:, :1].value_counts()
    df = df[(df.iloc[:, 34] == "Nashville, TN") & (df.iloc[:, 42] == "Chicago, IL")]
    df = df.iloc[: ,12]
    flag = df.empty
    if not flag:
        flag = df.empty
        if not flag:
            df = df.dropna()
            dictNew = df.to_dict()
            for key, val in dictNew.items():
                if val is not None:
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


def findAverage():
    sum = 0
    for var in result:
        print(var)
        sum += var

    mean = sum / len(result)
    return mean


def Thread_function(num_of_threads, readinginfo: list):
    thread_handle = []
    for j in range(0, num_of_threads):
        t = Thread((findAirtime(readinginfo[j])))
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
    result = []
    print(result)
    Thread_function(num_of_threads, readinginfo)
    print("\n Average time of flights from Nashville to Chicago: ", findAverage())
