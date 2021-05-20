"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above)

+

A simple Python script to send messages to a sever over Bluetooth
usingPython sockets (with Python 3.3 or above).

Configured by bluetoothPort.py

"""

import configparser
import socket
import os

config = configparser.ConfigParser()
config.read('bluetoothPort.ini')

serverMACAddress = config['DEFAULT']['macAddress']
port = config['DEFAULT']['port']
mode = config['DEFAULT']['mode']
backlog = config['DEFAULT']['backlog']
size = config['DEFAULT']['size']
inputFolder = config['DEFAULT']['input.folder']
outputFolder = config['DEFAULT']['output .folder']

server = socket.socket(
    socket.AF_BLUETOOTH,
    socket.SOCK_STREAM,
    socket.BTPROTO_RFCOMM
)

"""
S_ASK_DOWNLOAD -> {C_ANSWER_YES, C_ANSWER_NO}
C_ANSWER_YES -> clientUploadData & serverDownloadData
C_ANSWER_NO -> S_ASK_UPLOAD, S_ASK_WAIT
S_ASK_UPLOAD -> serverUploadData & clientDownloadData
S_ASK_WAIT -> clientSleep & serverSleep
"""

if (mode=="SERVER"):
    # SERVER mode
    server.bind((severMACAddress, port))
    server.listen(backlog)
    try:
        client, address = server.accept()
        while True:
            

    except:
	print("Closing socket")
	client.close()
	s.close()  
else:
    # CLIENT mode
    server.connect((serverMACAddress,port))
    while True:
        
    server.close()


def checkDataToSend(dir):
    dirPath = os.curdir + '/' + dir

    fileList = [f for f in os.listdir(dirPath) if
    os.path.isfile(os.path.join(dirPath, f))]

    # It returns the head
    return fileList[0:1]
