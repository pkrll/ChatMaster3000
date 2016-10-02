import urwid
from core.ui.components.wrapper import Wrapper

class TextField(urwid.Edit, Wrapper):
    """
        A text field

        This class extends the urwid widget Edit, that allows users to
        write and edit text.

        Args:
            delegate (obj)  :   The delegate.
    """
    delegate = None

    def __init__(self, caption='', delegate=None, align="left"):
        """
            Init

            Args:
                caption (str)   :   The caption of the edit box.
                delegate (obj)  :   The acting delegate.
        """
        self.delegate = delegate
        super(TextField, self).__init__(caption, align=align)

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
            super(TextField, self).keypress(size, key)
        else:
            if key == "enter":
                self.delegate.didReceiveReturnKeyEvent(self.edit_text)
            elif key in ("up", "down"):
                self.delegate.didReceiveArrowKeyEvent(key)
            else:
                super(TextField, self).keypress(size, key)
