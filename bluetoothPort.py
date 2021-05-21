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
import events

config = configparser.ConfigParser()
config.read('bluetoothPort.ini')

serverMACAddress = config['DEFAULT']['macAddress']
port = config['DEFAULT']['port']
mode = config['DEFAULT']['mode']
backlog = config['DEFAULT']['backlog']
size = config['DEFAULT']['size']
incomingFolder = config['DEFAULT']['input.folder']
outgoingFolder = config['DEFAULT']['output .folder']

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
            client.send(bytes(events.S_ASK_DOWNLOAD, "utf-8"))
            waitFor(client, [events.C_ANSWER_YES, events.C_ANSWER_NO])

            if response == events.C_ANSWER_YES:
                client.send(bytes(events.S_BEGIN, "utf-8"))
                data = client.recv(size)
                fileNameSizeStr = data.decode("utf-8")
                fileNameSize = fileNameSizeStr.split("-")
                fileName = fileNameSize[0]
                downloadSize = fileNameSize[1]
                file = open(fileName, "wb")
                data = client.recv(size)
                while downloadSize > 0:
                    downloadSize -= len(data)
                    file.write(data)
                    data = client.recv(size)
                file.close()
            

    except:
	print("Closing socket")
	client.close()
	s.close()  
else:
    # CLIENT mode
    server.connect((serverMACAddress,port))
    while True:
        waitFor(sever, [events.S_ASK_DOWNLOAD])
        
        fileList = checkDataToSend(incomingFolder)
        if not fileList:
            server.send(bytes(events.C_ANSWER_NO, "utf-8"))
        else:
            server.send(bytes(events.C_ANSWER_YES, "utf-8"))
            waitFor(sever, [events.S_BEGIN])
            
            server.send(bytes(fileList[0] + '-' + os.stat(fileList[0]).st_size, "utf-8"))
            
            print 'Sending: '+fileList[0]+'...'
            file = open(fileList[0],'rb')
            fileData = file.read(size)
            while (fileData):
                server.send(fileData)
                fileData = file.read(size)
            
            
    server.close()

def waitFor(host, eventList):
    event = -1
    while request not in eventList:
        data = host.recv(size);
        event = data.decode("utf-8")
    
    return event
    

def checkDataToSend(aDir):
    dirPath = os.curdir + '/' + aDir

    fileList = [f for f in os.listdir(dirPath) if
    os.path.isfile(os.path.join(dirPath, f))]

    # It returns the head
    return fileList[0:1]
