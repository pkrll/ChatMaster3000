import urwid
from core.ui.basicframe import BasicFrame
from core.ui.components.columnview import ColumnView
from core.ui.components.chatwindow import ChatWindow
from core.ui.components.channellist import ChannelList
from core.ui.components.chatbox import ChatBox
from core.ui.components.titlebar import TitleBar
from support.helpers import localTime
from support.const.globals import defaultPalette
from support.clock import Clock

class ChatFrame(BasicFrame):
    """
        Represents the main window frame of the application, which will consist
        of a ListBox widget (ChatWindow), Edit (ChatBox) and Text (TitleBar).
    """

    def __init__(self, delegate):
        """
            init
        """
        self.delegate = delegate
        # Create the components of the frame:
        titleBar = TitleBar(("titleBar", "ChatMaster 3000"), align="center")
        clock = urwid.AttrMap(Clock(self.delegate, align="right"), "titleBar")
        self.titleBar = ColumnView([('weight', 1, titleBar), (5, clock)])
        self.chatLog = ChatWindow()
        self.chatBox = ChatBox("> ", self)
        self.channelList = ChannelList()
        self.channelList.body.insert(0, urwid.Text(("channelList-text-bold", "Channels:")))
        # Wrap them with a display attribute. This will enable color application.
        header = self.titleBar.wrapWithAttribute("titleBar")
        footer = self.chatBox.wrapWithAttribute("footer")
        chatLog = self.chatLog.wrapWithAttribute("body")
        channelList = self.channelList.wrapWithAttribute("channelList")
        # Create a border between the channel list and the chat log
        channelListWithPadding = urwid.Padding(channelList, align="left", width=("relative", 95))
        channelListWithPadding = urwid.AttrMap(channelListWithPadding, "border")
        # Put them both in a columns widget
        self.columnView = ColumnView([(15, channelListWithPadding), ('weight', 1, chatLog)])
        # Call the super class and let it handle the heavy lifting.
        super(ChatFrame, self).__init__(self.columnView, header=header, footer=footer, focus_part='footer')

    def didReceiveReturnKeyEvent(self, parameter=None):
        """
        """
        self.delegate.didReceiveReturnKeyEvent(parameter)

    def didReceiveArrowKeyEvent(self, parameter=None):
        """
        """
        # Call the chat log's keypress method with the terminal dimensions
        if parameter is not None:
            self.chatLog.keypress(urwid.raw_display.Screen().get_cols_rows(), parameter)

    ##############################
    #   Component specific methods
    #############################

    def printToScreen(self, message, style="default"):
        """
            Print to the user's screen.

            Args:
                text    (string)   : The text to print out.
                style   (string)   : The style of the text.
        """
        time = localTime()
        time = "%s:%s" % (time.hour, time.minutes)
        message = "[%s] %s" % (time, message)
        textWidget = urwid.Text((style, message))
        currentRow = self.__numberOfRows()
        self.chatLog.body.insert(currentRow, textWidget)
        self.chatLog.focus_position = currentRow

    def printErrorMessage(self, errorMessage, style="bold-heading"):
        """
            Print out an error message.

            Args:
                errorMessage (str)  : The error message to display.
                style (str)         : The style.
        """
        self.printToScreen("Error: %s" % errorMessage, style)
        self.delegate.shouldUpdateScreen()

    def clearChatLog(self):
        """
            Clears the chat log.
        """
        self.chatLog.body[:] = []

    def enableChatBox(self, mode):
        """
            Enables or disables the chat box.

            Args:
                mode (bool) :   A bool representing whether the box should be enabled or not.
        """
        self.chatBox.isSelectable = mode
        if mode:
            self.set_focus("footer")
        else:
            self.set_focus("body")

    def setChatBoxCaption(self, caption):
        """
            Sets the chat box caption

            Args:
                caption (string) : The caption.
        """
        self.chatBox.set_caption(caption)

    def resetChatBox(self):
        """
            Resets the chat box.
        """
        self.chatBox.set_edit_text("")

    def clearChannelList(self):
        """
        """
        self.channelList.body[:] = []

    def setChannelList(self, channels):
        """
        """
        self.clearChannelList()
        self.channelList.body.insert(0, urwid.Text(("channelList-text-bold", "Channels:")))
        for channel in channels:
            self.channelList.body.append(urwid.Text(("channelList-text", channel)))
        self.delegate.shouldUpdateScreen()

    ##########################
    #   Semi-private methods
    ##########################

    def __numberOfRows(self):
        """
            Returns:
                The number of rows in the chat log.
        """
        return len(self.chatLog.body)
