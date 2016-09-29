import urwid
from twisted.internet import reactor
from core.client.chatclientfactory import ChatClientFactory
from core.ui.windowframe import WindowFrame
from support.const.globals import serverInformation, defaultPalette

class Application(object):
    """
        The ChatMaster 3000 application.

        Acts as the controller of the application, acting as the middle man
        between the UI (view) and the chat protocol (model, sort of...).

        Args:
            user (dict)         :   A dictionary consisting of the user's information.
            isConnected (bool)  :   A boolean value indicating whether the user is connected.
            clientFactory (obj) :   The chat protocol factory.
            frame (obj)         :   The UI frame of the application.
    """
    user = dict(username=None, id=None)
    isConnected = False
    clientFactory = None
    frame = None
    mainLoop = None

    def __init__(self):
        """
            Init

            Note:
                Before anything else, the __preliminaries() method will be called,
                setting up the client factory and the frame.
        """
        self.__preliminaries()
        self.__beginLoginProcess()
        self.mainLoop = urwid.MainLoop(self.frame, defaultPalette, event_loop=urwid.TwistedEventLoop())
        self.mainLoop.run()

    ##########################
    #   Event methods
    ##########################

    def didConnect(self):
        self.isConnected = True
        self.frame.clearChatLog()
        self.frame.printToScreen("Successfully connected.", "bold-heading")
        self.mainLoop.draw_screen()

    def didReceiveReturnKeyEvent(self, parameter=None):
        """
            Reacts on return key events.

            Invoked when the return key has been pressed.

            Args:
                parameter (str) :   The parameter sent along from the sending object.
                                    In most cases, the sending object will be the chat
                                    box, sending the user inputed string.
        """
        if parameter is None:
            return

        if isinstance(parameter, basestring):
            if self.isConnected is False:
                self.user["username"] = parameter
                self.__makeConnection()
            else:
                if parameter.startswith("/"):
                    self.__didReceiveCommand(parameter[1:])
                else:
                    text = "%s: %s" % (self.user["username"], parameter)
                    self.frame.printToScreen(text)
            self.frame.resetChatBox()

    def didReceiveArrowKeyEvent(self, parameter=None):
        pass

    def shouldUpdateScreen(self):
        self.mainLoop.draw_screen()

    ##########################
    #   Semi-private methods
    ##########################

    def __preliminaries(self):
        """
            Sets up the client factory and the frame.
        """
        self.clientFactory = ChatClientFactory(self)
        self.frame = WindowFrame(self)

    def __beginLoginProcess(self):
        """
            Begins the connection process where the user will be
            asked to input username.
        """
        self.frame.printToScreen("Please enter your username...", "bold-heading")
        self.frame.setChatBoxCaption("Username: ")

    def __makeConnection(self):
        """
            Attempts to connect to the server.
        """
        self.frame.setChatBoxCaption("> ")
        self.frame.clearChatLog()
        self.frame.printToScreen("Welcome %s. Attempting to connect to the server..." % self.user["username"])
        reactor.connectTCP(serverInformation["addr"], serverInformation["port"], self.clientFactory)

    def __didReceiveCommand(self, command):
        """
            Invoked when the user inputs a /command.

            Args:
                command (str)   :   The command.
        """
        if len(command) > 0:
            # Turn to lower case and split its arguments
            command = command.lower().split(" ")
            if command[0] == "exit":
                raise urwid.ExitMainLoop()
            elif command[0] == "clear":
                self.frame.clearChatLog()
            else:
                self.frame.printToScreen("[ Error: command %s not found. ]" % (command[0]), "bold-heading")
        else:
            self.frame.printToScreen("[ Error: No command given. ]", "bold-heading")
