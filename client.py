import socket
import pickle
import os
import config

import requests
import threading


# Connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((config.host, config.port))
sock.sendall(b"The HTTP multi-threaded files downloading client is ready")

# Get urls
data = pickle.loads(sock.recv(4096))


# The below code is used for each chunk of file handled
# by each thread for downloading the content from specified
# location to storage
def Handler(start, end, url, filename):
    # Specify the starting and ending of the file
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    print(headers)
    # Request the specified part and get into variable
    r = requests.get(url, headers=headers, stream=True)
    # Open the file and write the content of the html page
    # into file
    with open(filename, "r+b") as fp:
        fp.seek(start)
        fp.write(r.content)


def download_file(url_of_file, number_of_threads):

    r = requests.head(url_of_file)

    file_name = url_of_file.split('/')[-1]
    try:
        file_size = int(r.headers['content-length'])
    except ImportError:
        print("The URL is not correct")
        return

    part = int(file_size) / number_of_threads
    fp = open(file_name, "wb")
    fp.write(bytes('\0' * file_size, encoding="utf-8"))
    fp.close()

    for i in range(number_of_threads):
        start = int(part * i)
        end = start + part
        # Create a Thread with start and end locations
        t = threading.Thread(target=Handler, 
                kwargs={'start': start, 'end': end, 'url': url_of_file, 'filename': file_name})
        t.setDaemon(True)
        t.start()

    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s downloaded' % file_name)


if __name__ == '__main__':
    os.chdir(config.files_directory)
    for url in data:
        download_file(url, config.num_threads)
    # Close connecction
    sock.close()
