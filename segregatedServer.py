import socket
import collections
import time

#   ====================    FUNCTIONS    ====================    #
#   send a message to every connected client
def sendMessageToAllListeners( message, listeners ):
    #print( "the listeners listen..." )
    for listener in listeners:
        try:
            listener.send( message )
        except socket.timeout:
            pass
        except socket.error:
            #print( "\n!!! LISTENER DISCONNECTED !!!" )
            pass

#   check for new messages from clients
def checkForNewMessages( speakers, listeners ):
    #print( "checking for new messages..." )
    for speaker in speakers:
        bytesFromSpeaker = None
        try:
            bytesFromSpeaker = speaker.recv( 1024 )
            while bytesFromSpeaker:
                #print( "A traveler speaks..." )
                sendMessageToAllListeners( bytesFromSpeaker, listeners )
                bytesFromSpeaker = speaker.recv( 1024 )
        except socket.timeout:
            pass
        except socket.error:
            print( "\n!!! SPEAKER DISCONNECTED !!!" )
            bytesFromSpeaker = None

#   log new client joining to server terminal
def logNewClientJoining( clientType, newClientIPAddress ):
    print( time.strftime("%Y-%m-%d %H:%M"), " ", clientType, " joined. ", newClientIPAddress )

#   deal with new client connection
def dealWithNewClientConnection( newClientConnection, newClientIPAddress, speakers, listeners ):
    #   get client type
    newClientConnection.settimeout( 1.0 )
    bytesFromClient = newClientConnection.recv( 4 )
    clientType = bytesFromClient.decode()
    if clientType == "SPKR":
        newClientConnection.settimeout( 0.001 )
        speakers.append( newClientConnection )
        newClientConnection.send( speakerGreeting.encode() )
        logNewClientJoining( clientType, newClientIPAddress )
    if clientType == "LSTN":
        newClientConnection.settimeout( 0.001 )
        listeners.append( newClientConnection )
        newClientConnection.send( listenerGreeting.encode() )
        logNewClientJoining( clientType, newClientIPAddress )

#   check for new client connection
def checkForNewClientConnection( speakers, listeners ):
    #print( "checking for new travelers..." )
    newClientConnection = None
    newClientIPAddress = None
    try:
        newClientConnection, newClientIPAddress = serverSocket.accept()
    except socket.timeout:
        pass
    if newClientConnection is not None:
        dealWithNewClientConnection( newClientConnection, newClientIPAddress, speakers, listeners )


#   ====================    MAIN    ====================    #
#   -----   setup   -----   #
serverSocket = socket.socket()
serverSocket.settimeout( 5 )
#serverSocket.setblocking(0)
hostLocalIP = "10.0.0.43"
print( hostLocalIP )
port = 1337
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind( (hostLocalIP, port) )

speakerGreeting = "Welcome. We hear you."
listenerGreeting = "Welcome to Cyberia.\n present day\n present time              \n"

#   -----   setup state    -----   #
#   list of all connected clients
speakers = []
listeners = []

#   list of clients to be removed
disconnectedSpeakers = []
disconnectedListeners = []

#   newMesssages container
newMessages = collections.deque()

######!!!!! need to come up with a way to test for timeouts from all the connected clients periodically

#   -----   be a server -----   #
serverSocket.listen(5)
serverSocket.settimeout( 0.001 )
while True:
    checkForNewClientConnection( speakers, listeners )
    checkForNewMessages( speakers, listeners )
