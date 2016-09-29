import urwid
from core.ui.components.wrapper import Wrapper

class ChatBox(urwid.Edit, Wrapper):
    """
        The message box of the application.

        This class extends the urwid widget Edit, that allows users to
        write and edit text. The main window frame will be the delegate
        to this class.

        Args:
            caption (str)   :   The caption of the edit box.
            delegate (obj)  :   The acting delegate.
    """

    def __init__(self, caption='', delegate=None):
        self.delegate = delegate
        super(ChatBox, self).__init__(caption)

    def keypress(self, size, key):
        """
            Handles the keystrokes.

            Note:
                If a RETURN key is detected, the delegate method didPressReturn()
                should be invoked. The UP or DOWN keys will invoke the delegate
                method didReceiveKeyPress(). Other keystrokes will be sent up along
                chain to the parent class.
        """
        # TODO: Do it smarter.
        if self.delegate is None:
            super(ChatBox, self).keypress(size, key)
        else:
            if key == "enter":
                self.delegate.didReceiveReturnKeyEvent(self.edit_text)
            elif key in ("up", "down"):
                self.delegate.didReceiveArrowKeyEvent(key)
            else:
                super(ChatBox, self).keypress(size, key)
