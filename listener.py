import socket
import collections
import sys
import os
from sys import stdout
import time

#   ====================    FUNCTIONS    ====================    #
#   check for a message from the server
def checkForNewMessageFromServer( socketToServer ):
    bytesFromServer = None
    try:
        bytesFromServer = socketToServer.recv( 1024 )
        while bytesFromServer:
            stdout.buffer.write( bytesFromServer )
            stdout.flush()
            bytesFromServer = socketToServer.recv( 1024 )
    except socket.timeout:
        pass
    except BrokenPipeError:
        global serverOpen
        serverOpen = False
        print( "Alert:\tBrokenPipeError" )
        sys.exit()
    except socket.error:
        print( "Alert:\t Disconnected from server." )
        sys.exit()

#   see if the server is still connected
def pingServer( socketToServer ):
    #print( " pinging speakers " )
    try:
        socketToServer.send( "PING".encode() )
    except socket.timeout:
        pass
    except socket.error:
        print( "Server failed PING." )
        sys.exit()
        pass

#   keep track of time
def tic( lastTime, oneSecondTracker, socketToServer ):
    deltaTime = time.time() - lastTime
    oneSecondTracker += deltaTime

    if oneSecondTracker > 1:
        oneSecondTracker = 0
        pingServer( socketToServer )

    lastTime = time.time()

    return lastTime, oneSecondTracker

#   ====================    MAIN    ====================    #
#   -----   setup   -----   #
socketToServer = socket.socket( )
#socketToServer.setblocking(0)
host = "76.30.234.227"
port = 1337

#   time keepers
lastTime = time.time()
oneSecondTracker = 0

#   -----   connect to server   -----   #
socketToServer.settimeout(5)
socketToServer.connect( (host, port) )
clientType = "LSTN"
socketToServer.send( clientType.encode() )
bytesFromServer = socketToServer.recv( 1024 )
serverGreeting = bytesFromServer.decode()
stdout.write( serverGreeting )
stdout.flush()


#   -----   be a client -----   #
userMessage = None
bytesFromServer = None
socketToServer.settimeout( 0.001 )
serverOpen = True
while serverOpen:
    checkForNewMessageFromServer( socketToServer )
    lastTime, oneSecondTracker = tic( lastTime, oneSecondTracker, socketToServer )
