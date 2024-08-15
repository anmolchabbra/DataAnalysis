import pandas as pd
from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

global dataset
dataset = '../Combined_Flights_2021.csv'
N0_OF_TOTAL_ROWS = 631188


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
    start = time.time()
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

    print("\n Dates for which departure time is not recorded or missing: ")
    printDates(results)
    print(f'time taken with {size} workers (MPI execution): {round(time.time() - start, 2)} second(s)')


elif rank > 0:
    chunk_to_process = comm.recv()
    print(f'Worker {rank} is assigned chunk info {chunk_to_process} {dataset}')
    df = pd.read_csv(dataset, nrows=chunk_to_process[0], skiprows=chunk_to_process[1], header=None)
    df = df.loc[pd.isna(df[7])]
    result = df.iloc[:, 0]
    print(f'Worker slave {rank} is done. Sending back to master')
    comm.send(result, dest=0)

