from twisted.internet.protocol import Protocol
import json

class CMServer(Protocol):
    """
        The server protocol handles each new incoming connection.

        Args:
            username (str)  :   The username.
            channel  (str)  :   The channel the client is currently in.
    """

    username = None
    channel = None

    def __init__(self):
        pass

    def connectionMade(self):
        """
            Invoked when a new connection has been made.

            All new connections must be added to the factory, through
            the factory method addConnection().
        """
        self.factory.addConnection(self)
        self.sendRequest("login")

    def connectionLost(self, reason):
        """
            Invoked when a connection has been lost.

            Must call the factory method removeConnection().
        """
        self.factory.removeConnection(self)
        if self.channel is not None:
            self.factory.didLeaveChannel(self.channel, self.username)

    def dataReceived(self, data):
        """
            Received data.

            This method checks and parses the data received. The
            data can be either a message or a command package.

            Messages should be rerouted to the right channel, with the
            server factory method sendMessage(message, toChannel).

            Commands should be handled appropriately. See PROTOCOL.md
            for available commands.

            Args:
                data (json) : The data received.
        """
        data = json.loads(data)
        if data["type"] == "command":
            command = data["data"]["command"]
            if command == "login":
                username = data["data"]["parameters"]["username"]
                nameUnique = self.factory.isUsernameUnique(username)
                if nameUnique:
                    self.sendSession(nameUnique)
                    self.username = username
                else:
                    self.sendSession(nameUnique, "Username is already taken")
            # TODO: Add more commands
            elif command == "channel_list":
                self.sendChannelList()
            elif command == "join":
                channel = data["data"]["parameters"]["channel"]
                if self.channel != channel:
                    self.channel = data["data"]["parameters"]["channel"]
                    self.factory.didJoinChannel(self.channel, self.username)
                else:
                    self.sendError(command, "You have already joined the channel.")
            elif command == "leave":
                if self.channel is not None:
                    channel = self.channel
                    # The channel must be set to None before calling didLeave Channel
                    # as that method is sending out a notification to all users in the
                    # channel.
                    self.channel = None
                    self.factory.didLeaveChannel(channel, self.username)
                    self.sendChannelList()
                else:
                    self.sendError(command, "You are not in a channel.")
        elif data["type"] == "message":
            message = data["data"]["message"]
            self.factory.sendMessage(message, self.username, self.channel)

        # TODO: Add more package types

    def sendRequest(self, request):
        """
            Creates and sends a request message.

            Args:
                request (str) : The request to send.
        """
        data = json.dumps({
            "type": "request",
            "data": {
                "request": request
            }
        })

        self.transport.write(data)

    def sendSession(self, status, reason=None):
        """
            Send a session message.

            The session message indicates whether the client has
            successfully joined the server or not.

            The data attribute of a session message consists of two
            sub attributes:

                * status (with a boolean value),
                * reason (on failure) OR channels (on success)

            On success, the status attribute should be set to true,
            and the channels attribute consist of a list of public
            channels.

            On failure, the status attribute should be set to false,
            with a reason string.

            Args:
                The status
        """
        data = None
        if status is True:
            # Create session package
            # and retrieve channels list through appropriate factory method.
            channels = self.factory.channels
            data = json.dumps({
                "type": "session",
                "data": {
                    "status": status,
                    "channels": channels
                }
            })
        else:
            # Create session package
            # don't forget reason string
            data = json.dumps({
                "type": "session",
                "data": {
                    "status": status,
                    "reason": reason
                }
            })

        self.transport.write(data)

        # Don't forget to send it!

    def sendError(self, errorType, message):
        """
            Send an error message to the client.
        """
        data = json.dumps({
            "type": "error",
            "data": {
                "error_type": errorType,
                "message": message
            }
        })
        self.transport.write(data)

    def sendNotification(self, event_type, parameters=[]):
        """
            Send a notification to the client.
        """
        data = json.dumps({
            "type": "notification",
            "data": {
                "event_type": event_type,
                "parameters": parameters
            }
        })

        self.transport.write(data)

    def sendMessage(self, message, username):
        """
            Send a message to the client.
        """
        data = json.dumps({
            "type": "message",
            "data": {
                "message": message,
                "username": username
            }
        })

        self.transport.write(data)

    def sendChannelList(self):
        """
            Send the current channels list.
        """
        self.sendNotification("channel_list", {"channels": self.factory.channels})
