from twisted.internet import protocol
from core.client.chatclient import ChatClient

class ChatClientFactory(protocol.ClientFactory):
    """
        The ChatMaster 3000 Client Factory.

        This class is will be generating new instances of the ChatMaster
        3000 client protocol, that will be responsible for handling the
        actual communication between the server and the user.
    """

    protocol = ChatClient
    delegate = None
    username = None

    def __init__(self, delegate=None):
        self.delegate = delegate

    def setUsername(self, username):
        self.username = username

    def buildProtocol(self, addr):
        """
            Creates an instance of the ChatClient protocol. Invoked when
            the user attempts to connect to the server.

            Returns:
                An instance of the chat client protocol.
        """
        return self.protocol(self.username, self.delegate)

    def clientConnectionFailed(self, connector, reason):
        """
            Called when the connection has failed.
        """
        self.delegate.didFailConnection(reason.getErrorMessage())
