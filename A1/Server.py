import socket
import random
import string
import struct
from threading import Thread
import os
import pandas as pd

from pathlib import Path

global dataset
dataset = 'C:/Users/nalin/Desktop/Combined_Flights_2021.csv'

N0_OF_TOTAL_ROWS = 6311871
def get_working_directory_info(working_directory):
    """
    Creates a string representation of a working directory and its contents.
    :param working_directory: path to the directory
    :return: string of the directory and its contents.
    """
    dirs = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_dir()])
    files = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_file()])
    dir_info = f'Current Directory: {working_directory}:\n|{dirs}{files}'
    return dir_info


def generate_random_eof_token():
    """Helper method to generates a random token that starts with '<' and ends with '>'.
     The total length of the token (including '<' and '>') should be 10.
     Examples: '<1f56xc5d>', '<KfOVnVMV>'
     return: the generated token.
     """
    #t = '<KfOVnVMV>'
    """thislist = list(string.ascii_letters)
    thislist.append(string.digits)
    result_str = random.choices(list, 8)"""

    t = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))
    t = '<' + t + '>'
    #print(t)
    return t
    #raise NotImplementedError('Your implementation here.')


def receive_message_ending_with_token(active_socket, buffer_size, eof_token):
    """
    Same implementation as in receive_message_ending_with_token() in client.py
    A helper method to receives a bytearray message of arbitrary size sent on the socket.
    This method returns the message WITHOUT the eof_token at the end of the last packet.
    :param active_socket: a socket object that is connected to the server
    :param buffer_size: the buffer size of each recv() call
    :param eof_token: a token that denotes the end of the message.
    :return: a bytearray message with the eof_token stripped from the end.
    """
    data = bytearray()
    while True:
        packet = active_socket.recv(buffer_size)
        if packet[-10:] == str(eof_token).encode():
            data += packet[:-10]
            #print("3 receiving")
            break
        data += packet
    return data

    #raise NotImplementedError('Your implementation here.')


def handle_request(rating):


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
        # leftOver = N0_OF_TOTAL_ROWS % numberOfThreads
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
        # print("Length", len(unique_res))
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
        num_of_threads = 2
        readinginfo = []
        readinginfo = distribute_chunks(num_of_threads)
        result = []
        print('Processing...')
        Thread_function(num_of_threads, readinginfo)
        print("\n Dates for which departure time is not recorded or missing: ")
        printDates()
        print(
            f'time taken with {num_of_threads} threads (Multithreading execution): {round(time.time() - start, 2)} second(s)')

    #print(f'Sent the contents of "{file_name.decode()}" to: {self.address}')
    #self.service_socket.close()
    #raise NotImplementedError('Your implementation here.')


class ClientThread(Thread):
    def __init__(self, service_socket : socket.socket, address : str):
        Thread.__init__(self)
        self.service_socket = service_socket
        self.address = address

    def run(self):
        # print ("Connection from : ", self.address)
        print("Connection from: ", self.address)
        #raise NotImplementedError('Your implementation here.')

        # initialize the connection
        # send random eof token
        token = generate_random_eof_token()

        self.service_socket.sendall(str.encode(token))

        # establish working directory

        homeDirectory = os.getcwd()

        os.chdir(homeDirectory)
        # send the current dir info
        """dir = homeDirectory + token
        print("Directory", dir)
        self.service_socket.sendall(dir.encode())"""

        # while True:
        while True:
            # get the command and arguments and call the corresponding method
            cwd = get_working_directory_info(os.getcwd())
            # send current dir info
            dir = cwd + token
            #print("Directory", dir)
            self.service_socket.sendall(dir.encode())
            msg = "Give the rating for which you want to find books?"
            self.service_socket.sendall(msg.encode())
            data = receive_message_ending_with_token(self.service_socket, 1024, token)
            #print(1)
            dataReceived = data.decode()
            if dataReceived == "exit":
                break
            handle_request(dataReceived)

        self.service_socket.close()
        print('Connection closed from:', self.address)

def main():
    HOST = "172.17.0.2"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        #print("binded to ", HOST + " and port number ", PORT)
        s.listen()
        while True:
            conn, addr = s.accept()
            client_thread = ClientThread(conn, addr)
            #client_thread.daemon = True
            client_thread.start()
        #raise NotImplementedError('Your implementation here.')



if __name__ == '__main__':
    main()

