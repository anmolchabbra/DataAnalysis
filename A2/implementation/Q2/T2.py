import time
import multiprocessing
import pandas as pd
from multiprocessing import Pool

global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'

N0_OF_TOTAL_ROWS = 6311871
def map_tasks(readingItem: list):
    df = pd.read_csv(dataset, nrows=readingItem[0], skiprows=readingItem[1], header=None, low_memory=False)
    # return df.iloc[:, :1].value_counts()
    df = df[(df.iloc[:, 0] >= "2021-11-20") & (df.iloc[:, 0] <= "2021-11-30")]
    df = df[df.iloc[:, 5] == True]
    df = df.iloc[:, [0, 1, 5]]
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

def findSum(resultDict):
    sum = 0
    for key, value in resultDict.items():
        sum += resultDict[key]
    return sum

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

    print('Processing...')
    processes = multiprocessing.cpu_count()
    p = Pool(processes=processes)
    result = p.map(map_tasks, distribute_chunks(processes))
    ans = reduce_task(result)

    print("\n Diverted flights bw 20th Nov and 30th Nov 2021: ", findSum(ans))
    p.close()
    p.join()

if __name__ == '__main__':
    compute_multiprocessing()
