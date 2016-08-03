from tkinter import Tk, Canvas
from PIL import ImageTk
from screenshot.pyrobot import Robot

_r = Robot()


def take_screenshot_whole(path):
    pimage = _r.take_screenshot()
    pimage.save(path, "PNG")


def take_screenshot_crop(path):
    pimage = _r.take_screenshot()

    _, _, width, height = pimage.getbbox()

    root = Tk()  # Creates a Tkinter window
    root.overrideredirect(True)  # Makes the window borderless
    root.geometry("{0}x{1}+0+0".format(width, height))  # Makes the window the same size as the taken screenshot
    root.config(cursor="crosshair")  # Sets the cursor to a crosshair

    pimage_tk = ImageTk.PhotoImage(pimage)  # Converts the PIL.Image into a Tkinter compatible PhotoImage

    can = Canvas(root, width=width, height=height)  # Creates a canvas object on the window
    can.pack()
    can.create_image((0, 0), image=pimage_tk, anchor="nw")  # Draws the screenshot onto the canvas

    # This class holds some information about the drawn rectangle
    class CanInfo:
        rect = None
        startx, starty = 0, 0

    # Stores the starting position of the drawn rectangle in the CanInfo class
    def xy(event):
        CanInfo.startx, CanInfo.starty = event.x, event.y

    # Redraws the rectangle when the cursor has been moved
    def capture_motion(event):
        can.delete(CanInfo.rect)
        CanInfo.rect = can.create_rectangle(CanInfo.startx, CanInfo.starty, event.x, event.y)

    # Saves the image when the user releases the left mouse button
    def save_img(event):
        startx, starty = CanInfo.startx, CanInfo.starty
        endx, endy = event.x, event.y

        # Puts the starting point in the upper left and the ending point in the lower right corner of the rectangle
        if startx > endx:
            startx, endx = endx, startx
        if starty > endy:
            starty, endy = endy, starty

        crop_image = pimage.crop((startx, starty, endx, endy))
        crop_image.save(path, "PNG")
        root.destroy()  # Closes the Tkinter window

    # Binds mouse actions to the functions defined above
    can.bind("<Button-1>", xy)
    can.bind("<B1-Motion>", capture_motion)
    can.bind("<ButtonRelease-1>", save_img)

    root.mainloop()  # Shows the Tk window and loops until it is closed