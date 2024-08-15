import time

import pandas as pd
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

global dataset
dataset = '../Combined_Flights_2021.csv'
N0_OF_TOTAL_ROWS = 631188


def reduce_task(results):
    out = {}
    for r in results:
        first = r.to_dict()
        for key, value in r.to_dict().items():
            for key1, value1 in first[key].items():
                if key in out:
                    out[key1] = out[key1] + value1
                else:
                    out[key1] = value1
    return out

def findSum(resultDict: dict):
    sum = 0
    for key, value in resultDict.items():
        sum += resultDict[key]
    return sum


if rank == 0:
    """
    Master worker (with rank 0) is responsible for distributes the workload evenly 
    between slave workers.
    """


    def distribute_chunks(numberOfCalls: int):
        start = 1
        reading_info = []
        n_rows = N0_OF_TOTAL_ROWS / numberOfCalls
        # leftOver = N0_OF_TOTAL_ROWS % numberOfThreads
        for i in range(0, numberOfCalls):
            if (i == numberOfCalls - 1):
                reading_info.append([None, int(start)])
            else:
                reading_info.append([int(n_rows), int(start)])
                start += n_rows
        return reading_info

    slave_workers = size - 1
    chunk_distribution = distribute_chunks(slave_workers)

    # distribute tasks to slaves
    for worker in range(1, size):
        chunk_to_process = worker-1
        comm.send(chunk_distribution[chunk_to_process], dest=worker)

    # receive and aggregate results from slave
    results = []
    startTime = time.time()
    for worker in (range(1, size)):  # receive
        result = comm.recv(source=worker)
        results.append(result)
        #print(f'received from Worker slave {worker}')

    out = {}
    out = reduce_task(results)

    print("\n Diverted flights bw 20th Nov and 30th Nov 2021: ", findSum(out))
    endTime = time.time()
    print("Time taken w : " + str(endTime - startTime))


elif rank > 0:
    chunk_to_process = comm.recv()
    print(f'Worker {rank} is assigned chunk info {chunk_to_process} {dataset}')
    df = pd.read_csv(dataset, nrows=chunk_to_process[0], skiprows=chunk_to_process[1], header=None)
    df = df[(df.iloc[:, 0] >= "2021-11-20") & (df.iloc[:, 0] <= "2021-11-30")]
    df = df[df.iloc[:, 5] == True]
    df = df.iloc[:, [0, 1, 5]]
    result = pd.DataFrame(df.iloc[:, 1].value_counts())
    print(f'Worker slave {rank} is done. Sending back to master')
    comm.send(result, dest=0)

