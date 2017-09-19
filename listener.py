import socket
import collections
import os
from sys import stdin

#   ====================    FUNCTIONS    ====================    #
#   deal with newly received message from server
def dealWithNewMessageFromServer( messageFromServer, socketToServer ):
    #   this is where we would see what the message type is or something
    print( messageFromServer, end = '' )

#   check for a message from the server
def checkForNewMessageFromServer( socketToServer ):
    bytesFromServer = None
    try:
        bytesFromServer = socketToServer.recv( 1024 )
        if bytesFromServer is not None:
            messageFromServer = bytesFromServer.decode()
            dealWithNewMessageFromServer( messageFromServer, socketToServer )
    except socket.timeout:
        pass
    except BrokenPipeError:
        global serverOpen
        serverOpen = False
        print( "\n!!!!! SERVER DISCONNECTED !!!!!" )


#   ====================    MAIN    ====================    #
#   -----   setup   -----   #
socketToServer = socket.socket( )
#socketToServer.setblocking(0)
host = "76.30.234.227"
port = 1337

#   -----   connect to server   -----   #
socketToServer.settimeout(5)
socketToServer.connect( (host, port) )
clientType = "LSTN"
socketToServer.send( clientType.encode() )
bytesFromServer = socketToServer.recv( 1024 )
serverGreeting = bytesFromServer.decode()
print( serverGreeting )

#   -----   be a client -----   #
userMessage = None
bytesFromServer = None
socketToServer.settimeout( 0.001 )
serverOpen = True
while serverOpen:
    checkForNewMessageFromServer( socketToServer )
