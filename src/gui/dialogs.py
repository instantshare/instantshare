import tkinter
import tkinter.simpledialog


def text_input(title: str, message: str, hidden=False):
    root = tkinter.Tk()
    root.withdraw()

    if hidden:
        entered_text = tkinter.simpledialog.askstring(title=title, prompt=message, show='*')
    else:
        entered_text = tkinter.simpledialog.askstring(title, message)

    root.destroy()
    return entered_text
