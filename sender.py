import socket
import shutil
import timeit
import os
import sys
import tqdm

SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 16384

host = sys.argv [1]

port = 5001

print(sys.argv)
file_name = sys.argv [2] 
if os.path.isdir(file_name):
	shutil.make_archive(file_name, 'zip', file_name)
	file_name = file_name + '.zip'

file_size = os.path.getsize(file_name)

sender_socket = socket.socket()

sender_socket.connect((host, port))

sender_socket.send(f'{file_name}{SEPARATOR}{file_size}'.encode())

progress = tqdm.tqdm(range(file_size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

with open(file_name, 'rb') as le_file:
	start = timeit.default_timer()
	while True:
		chunk = le_file.read(BUFFER_SIZE)
		if not chunk:
			print('inside the if block, thus, terminating')
			break
		sender_socket.sendall(chunk)
		progress.update(len(chunk))
	stop = timeit.default_timer()

print(f'time required for transferring : {stop - start}')
sender_socket.close()
