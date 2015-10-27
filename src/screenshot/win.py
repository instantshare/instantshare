# https://github.com/chriskiehl/pyrobot
# started from Audionautics code on
# http://stackoverflow.com/questions/3585293/pil-imagegrab-fails-on-2nd-virtual-monitor-of-virtualbox
# updated for PILLOW and Python 3 by Alan Baines (Kizrak)

from ctypes import *
from ctypes.wintypes import *
import sys


def get_screen_buffer(bounds=None):
    # Grabs a DC to the entire virtual screen, but only copies to
    # the bitmap the the rect defined by the user.

    SM_XVIRTUALSCREEN = 76  # coordinates for the left side of the virtual screen.
    SM_YVIRTUALSCREEN = 77  # coordinates for the right side of the virtual screen.
    SM_CXVIRTUALSCREEN = 78 # width of the virtual screen
    SM_CYVIRTUALSCREEN = 79 # height of the virtual screen

    hDesktopWnd = windll.user32.GetDesktopWindow()   # Entire virtual Screen

    left = windll.user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
    top = windll.user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
    width = windll.user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    height = windll.user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)

    if bounds:
        left, top, right, bottom = bounds
        width = right - left
        height = bottom - top

    hDesktopDC = windll.user32.GetWindowDC(hDesktopWnd)
    if not hDesktopDC:
        print('GetDC Failed')
        sys.exit()

    hCaptureDC = windll.gdi32.CreateCompatibleDC(hDesktopDC)
    if not hCaptureDC:
        print('CreateCompatibleBitmap Failed')
        sys.exit()

    hCaptureBitmap = windll.gdi32.CreateCompatibleBitmap(hDesktopDC, width, height)
    if not hCaptureBitmap:
        print('CreateCompatibleBitmap Failed')
        sys.exit()

    windll.gdi32.SelectObject(hCaptureDC, hCaptureBitmap)

    windll.gdi32.BitBlt(
        hCaptureDC,
        0, 0,
        width, height,
        hDesktopDC,
        left, top,
        0x00CC0020
    )
    return hCaptureBitmap


def make_image_from_buffer(hCaptureBitmap):
    from PIL import Image
    bmp_info = BITMAPINFO()
    hdc = windll.user32.GetDC(None)

    bmp_info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER)

    DIB_RGB_COLORS = 0
    windll.gdi32.GetDIBits(hdc,
        hCaptureBitmap,
        0, 0,
        None, byref(bmp_info),
        DIB_RGB_COLORS
    )

    bmp_info.bmiHeader.biSizeImage = int( bmp_info.bmiHeader.biWidth *abs(bmp_info.bmiHeader.biHeight) * (bmp_info.bmiHeader.biBitCount+7)/8 );
    size = (bmp_info.bmiHeader.biWidth, bmp_info.bmiHeader.biHeight )
    pBuf = (c_char * bmp_info.bmiHeader.biSizeImage)()

    windll.gdi32.GetBitmapBits(hCaptureBitmap, bmp_info.bmiHeader.biSizeImage, pBuf)

    return Image.frombuffer('RGB', size, pBuf, 'raw', 'BGRX', 0, 1)


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', ctypes.c_uint32),
        ('biWidth', ctypes.c_int),
        ('biHeight', ctypes.c_int),
        ('biPlanes', ctypes.c_short),
        ('biBitCount', ctypes.c_short),
        ('biCompression', ctypes.c_uint32),
        ('biSizeImage', ctypes.c_uint32),
        ('biXPelsPerMeter', ctypes.c_long),
        ('biYPelsPerMeter', ctypes.c_long),
        ('biClrUsed', ctypes.c_uint32),
        ('biClrImportant', ctypes.c_uint32)
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', ctypes.c_ulong * 3)
    ]

def take_screenshot(path):
    hCaptureBitmap = get_screen_buffer()

    pimage = make_image_from_buffer(hCaptureBitmap)

    pimage.save(path,"PNG")