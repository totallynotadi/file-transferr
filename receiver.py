import socket
import os
import sys
import tqdm
import timeit

host = socket.gethostbyname(socket.gethostname())
print(f'the host IP is : {host}')

port = 5001

BUFFER_SIZE = 16384
SEPARATOR = '<SEPARATOR>'
receiver_socket = socket.socket()

receiver_socket.bind((host, port))

receiver_socket.listen(5)

sender_socket, address = receiver_socket.accept()

received = sender_socket.recv(BUFFER_SIZE).decode()

file_name, file_size = received.split(SEPARATOR)
print(f'file name : {file_name}')
print(f'file size : {file_size}')

progress = tqdm.tqdm(range(int(file_size)), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

with open('C:\\Users\\gadit\\file_tran\\' + file_name, 'wb') as le_file:
	start = timeit.default_timer()
	while True:
		read_chunk = sender_socket.recv(BUFFER_SIZE)
		if not read_chunk:
			break
		le_file.write(read_chunk)
		progress.update(len(read_chunk))
	stop = timeit.default_timer()

print(f'time for receiving the file : {stop - start}')

sender_socket.close()
receiver_socket.close()