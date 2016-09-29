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

    def __init__(self, delegate=None):
        self.delegate = delegate

    def buildProtocol(self, addr):
        """
            Creates an instance of the ChatClient protocol. Invoked when
            the user attempts to connect to the server.

            Returns:
                An instance of the chat client protocol.
        """
        return self.protocol(self.delegate)
