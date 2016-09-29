from twisted.internet import protocol

class ChatClient(protocol.Protocol):
    """
        The ChatMaster 3000 client protocol.

        The client protocol is responsible for handling the communication
        between the server and the user.

        Args:
            delegate (obj)  :   The delegate of the client.
    """

    delegate = None

    def __init__(self, delegate=None):
        """
            Initializes the object and sets the delegate.

            Note:
                The delegate will be notified upon events.
        """
        self.delegate = delegate

    def connectionMade(self):
        if self.delegate is not None:
            self.delegate.didConnect()

    def connectionLost(self, reason):
        if self.delegate is not None:
            self.delegate.didLoseConnection(reason.getErrorMessage())
