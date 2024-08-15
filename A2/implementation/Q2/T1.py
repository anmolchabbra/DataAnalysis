from threading import Thread
import pandas as pd


global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'

N0_OF_TOTAL_ROWS = 6311871
def findDivertedFlight(readingItem: list):
    df = pd.read_csv(dataset, nrows=readingItem[0], skiprows=readingItem[1], header=None, low_memory=False)
    # return df.iloc[:, :1].value_counts()
    df = df[(df.iloc[:, 0] >= "2021-11-20") & (df.iloc[:, 0] <= "2021-11-30")]
    df = df[df.iloc[:, 5] == True]
    df = df.iloc[:, [0, 1, 5]]
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

def distribute_chunks(numberOfThreads: int):
    start = 1
    reading_info = []
    n_rows = N0_OF_TOTAL_ROWS / numberOfThreads
    for i in range(0, numberOfThreads):
        if (i == numberOfThreads - 1):
            reading_info.append([None, int(start)])
        else:
            reading_info.append([int(n_rows), int(start)])
            start += n_rows
    return reading_info

def findSum():
    sum = 0
    for key, value in result.items():
        sum += result[key]
    return sum


def Thread_function(num_of_threads, readinginfo: list):
    thread_handle = []
    for j in range(0, num_of_threads):
        t = Thread((findDivertedFlight(readinginfo[j])))
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
    print("\n Diverted flights bw 20th Nov and 30th Nov 2021: ", findSum())
