import socket
import collections
import os
import errno
import sys
import time
from sys import stdin
from select import select

#   ====================    FUNCTIONS    ====================    #
#   check for a new message from the user
def checkForMessageFromUser( socketToServer ):
    userMessage = None
    containsStdinIfHasData, _, _ = select( [stdin], [], [], 0.01 )
    if containsStdinIfHasData:
        userMessage = stdin.readline()
    if userMessage is not None:
        try:
            socketToServer.send( userMessage.encode() )
        except:
            print( "Alert:\tDisconnected from server." )
            sys.exit()

#   see if the server is still connected
def unpingServer( socketToServer ):
    #print( " pinging server " )
    try:
        ping = socketToServer.recv( 1024 )
        while ping:
            ping = socketToServer.recv( 1024 )
    except socket.timeout:
        pass
    except BrokenPipeError:
        global serverOpen
        serverOpen = False
        print( "Alert:\tBrokenPipeError" )
        sys.exit()
    except socket.error:
        print( "Server failed PING." )
        sys.exit()

#   keep track of time
def tic( lastTime, oneSecondTracker, socketToServer ):
    deltaTime = time.time() - lastTime
    oneSecondTracker += deltaTime

    if oneSecondTracker > 1:
        oneSecondTracker = 0
        unpingServer( socketToServer )

    lastTime = time.time()

    return lastTime, oneSecondTracker


#   ====================    MAIN    ====================    #
#   -----   state   -----   #
socketToServer = socket.socket()

#   -----   constants   -----   #
host = "76.30.234.227"
port = 1337
clientType = "SPKR"

#   time keepers
lastTime = time.time()
oneSecondTracker = 0

#   -----   connect to server   -----   #
socketToServer.settimeout(5)
socketToServer.connect( (host, port) )
socketToServer.send( clientType.encode() )
bytesFromServer = socketToServer.recv( 1024 )
serverGreeting = bytesFromServer.decode()
print( serverGreeting )

#   -----   be a client -----   #
socketToServer.settimeout( 0.001 )
while True:
    checkForMessageFromUser( socketToServer )
    lastTime, oneSecondTracker = tic( lastTime, oneSecondTracker, socketToServer )
