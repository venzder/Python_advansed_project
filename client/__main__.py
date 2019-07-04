import zlib
import yaml
import json
import socket
import threading
import hashlib
from datetime import datetime
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file'
)
parser.add_argument(
    '-m', '--mode', type=str, default='w',
    help='Sets client mode'
)

args = parser.parse_args()

host = 'localhost'
port = 8000
buffersize = 1024
encoding = 'utf-8'


def read():
    while True:
        response = sock.recv(buffersize)
        b_response = zlib.decompress(response)
        print(b_response.decode(encoding))


def write():
    while True:
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode(encoding)
        )

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = {
            'action': action,
            'data': data,
            'time': datetime.now().timestamp(),
            'user': hash_obj.hexdigest()
        }
        s_request = json.dumps(request)
        b_request = zlib.compress(s_request.encode(encoding))
        sock.send(b_request)


if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

try:
    sock = socket.socket()
    sock.connect((host, port))
    print('Client started')
    if args.mode == 'w':
        write()
    elif args.mode == 'rw':
        rthread = threading.Thread(target=read, daemon=True)
        rthread.start()
        write()
    else:
        read()
except KeyboardInterrupt:
    pass
