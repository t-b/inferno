#uses win32gui to controler recalcitrant API-less datasources >_<
#XXX broken due to inability to focus window

from time import sleep

import win32gui as wig
import win32ui as wui
import win32con as wic
from win32api import SetCursorPos, mouse_event
def getWindows():
    """ Get a list of all the windows. List of tuples (int, string)
    the string is the window name. """
    toplist=[]
    winlist=[]

    def enum_callback(hwnd, results):
        winlist.append((hwnd,wig.GetWindowText(hwnd)))

    wig.EnumWindows(enum_callback, toplist)

    return winlist

def getWindowFromName(name):
    return wui.FindWindow(None,name)

def getLeftBottom(window):
    return window.GetWindowRect()[0::3] #left,top,right,bottom

def getLeftTop(window):
    return window.GetWindowRect()[:2]

def clickMouse(x,y,timeDown=.1): #FIXME need a way to change focus back to the original window!
    """click ye mouse"""
    mX,mY=wig.GetCursorPos() #save the position so we can return to it
    SetCursorPos((x,y))
    mouse_event(wic.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    sleep(timeDown)
    mouse_event(wic.MOUSEEVENTF_LEFTUP,x,y,0,0)
    SetCursorPos((mX,mY))

def clickButton(WindowLeftTop,ButtonOffset):
    x=WindowLeftTop[0]+ButtonOffset[0]
    y=WindowLeftTop[1]+ButtonOffset[1]
    clickMouse(x,y,timeDown=.1)

def main():
    clickButton( getLeftTop( getWindowFromName( getWindows()[0][1] ) ) , (100,100) )
if __name__ == '__main__':
    main()


