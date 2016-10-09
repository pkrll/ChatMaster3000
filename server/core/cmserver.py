from twisted.internet.protocol import Protocol
import json

class CMServer(Protocol):
    """
        The server protocol handles each new incoming connection.

        Args:
            username (str)  :   The username.
            room     (str)  :   The room the client is currently in.
    """

    username = None
    room = None

    def __init__(self):
        pass

    def connectionMade(self):
        """
            Invoked when a new connection has been made.

            All new connections must be added to the factory, through
            the factory method addConnection().
        """
        pass

    def connectionLost(self, reason):
        """
            Invoked when a connection has been lost.

            Must call the factory method removeConnection().
        """
        pass

    def dataReceived(self, data):
        """
            Received data.

            This method checks and parses the data received. The
            data can be either a message or a command package.

            Messages should be rerouted to the right room, with the
            server factory method sendMessage(message, inRoom).

            Commands should be handled appropriately. See PROTOCOL.md
            for available commands.

            Args:
                data (json) : The data received.
        """
        pass


    def sendRequest(self, request):
        """
            Creates and sends a request message.

            Args:
                request (str) : The request to send.
        """
        pass

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
            rooms.

            On failure, the status attribute should be set to false,
            with a reason string.

            Args:
                The status
        """
        if status is True:
            # Create session package
            # and retrieve channels list through appropriate factory method.
            pass
        else:
            # Create session package
            # don't forget reason string
            pass

        # Don't forget to send it!
