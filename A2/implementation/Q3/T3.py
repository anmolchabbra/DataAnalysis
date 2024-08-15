import pandas as pd
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

global dataset
dataset = '../Combined_Flights_2021.csv'
N0_OF_TOTAL_ROWS = 631188


def findAverage(result):
    sum = 0
    len = 0
    for value in result:
        for value1 in value:
            sum += value1
            len += 1

    mean = sum / len
    return mean


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


    startTime = time.time()
    slave_workers = size - 1
    chunk_distribution = distribute_chunks(slave_workers)

    # distribute tasks to slaves
    for worker in range(1, size):
        chunk_to_process = worker-1
        comm.send(chunk_distribution[chunk_to_process], dest=worker)

    # receive and aggregate results from slave
    results = []
    for worker in (range(1, size)):  # receive
        result = comm.recv(source=worker)
        results.append(result)
        #print(f'received from Worker slave {worker}')

    print("\n Average time of flights from Nashville to Chicago: ", findAverage(results))
    endTime = time.time()
    print("Time taken w : " + str(endTime - startTime))

elif rank > 0:
    chunk_to_process = comm.recv()
    print(f'Worker {rank} is assigned chunk info {chunk_to_process} {dataset}')
    df = pd.read_csv(dataset, nrows=chunk_to_process[0], skiprows=chunk_to_process[1], header=None)
    df = df[(df.iloc[:, 34] == "Nashville, TN") & (df.iloc[:, 42] == "Chicago, IL")]
    df = df.iloc[:, 12]
    df = df.dropna()
    result = df.to_list()
    print(f'Worker slave {rank} is done. Sending back to master')
    comm.send(result, dest=0)

