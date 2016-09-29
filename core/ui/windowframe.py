import urwid
from core.ui.components.chatwindow import ChatWindow
from core.ui.components.chatbox import ChatBox
from core.ui.components.titlebar import TitleBar
from support.const.globals import defaultPalette

class WindowFrame(urwid.Frame):
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
        self.chatLog = ChatWindow()
        self.chatBox = ChatBox("> ", self)
        self.titleBar = TitleBar(("bold-heading", "ChatMaster 3000"), align="center")
        # Wrap them with a display attribute. This will enable color application.
        header = self.titleBar.wrapWithAttribute("bold-heading")
        footer = self.chatBox.wrapWithAttribute("footer")
        body = self.chatLog.wrapWithAttribute("body")
        # Call the super class and let it handle the heavy lifting.
        super(WindowFrame, self).__init__(body, header=header, footer=footer, focus_part='footer')

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
        textWidget = urwid.Text((style, message))
        currentRow = self.__numberOfRows()
        self.chatLog.body.insert(currentRow, textWidget)
        self.chatLog.focus_position = currentRow

    def clearChatLog(self):
        """
            Clears the chat log.
        """
        self.chatLog.body[:] = []

    def enableChatBox(self, mode):
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

    ##########################
    #   Semi-private methods
    ##########################

    def __numberOfRows(self):
        """
            Returns:
                The number of rows in the chat log.
        """
        return len(self.chatLog.body)
