#uses win32gui to controler recalcitrant API-less datasources >_<
#XXX broken due to inability to focus window

from time import sleep

import win32gui as wig
import win32ui as wui
import win32con as wic
from win32api import SetCursorPos, mouse_event

#empirically determined offsets from the top left corner

#protocols
#y offset 140

def make_offsets():
    """ offsets measured from the LEFT & TOP edges,
        aka the (x,y) of the top left corner
        this is actually a really obfusticated way to do this
        but if something changes it could be useful """
    PROT_Y_OFFSET=140
    #x values
    BUTTON_WIDTH=27
    G1_START=305
    G2_START=400
    G3_START=495
    #number of buttons per group
    G1_COUNT=8
    G2_COUNT=3
    G3_COUNT=3

    g1={ 1+n:( G1_START + BUTTON_WIDTH * n , PROT_Y_OFFSET) for n in range(G1_COUNT) }

    g2={ 1+n+G1_COUNT:( G2_START + BUTTON_WIDTH * n , PROT_Y_OFFSET) for n in range(G2_COUNT) }
    g3={ 1+n+G1_COUNT+G2_COUNT:( G2_START + BUTTON_WIDTH * n , PROT_Y_OFFSET) for n in range(G3_COUNT) }

    offsetDict={ 'record':(355,70) }
    offsetDict.update(g1)
    offsetDict.update(g2)
    offsetDict.update(g3)
    return offsetDict

PCLAMP_BUTTON_OFFSETS = make_offsets()


def get_windows():
    toplist=[]
    winlist=[]

    def enum_callback(hwnd, results):
        winlist.append((hwnd,wig.GetWindowText(hwnd)))

    wig.EnumWindows(enum_callback, toplist)
    return winlist


def getLeftBottom(window):
    return window.GetWindowRect()[0::3] #left,top,right,bottom

def getLeftTop(window):
    return window.GetWindowRect()[:2]

def clickMouse(x,y,slp=.1): #FIXME need a way to change focus back to the original window!
    """click ye mouse"""
    mX,mY=wig.GetCursorPos() #save the position so we can return to it
    SetCursorPos((x,y))
    mouse_event(wic.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    sleep(slp)
    mouse_event(wic.MOUSEEVENTF_LEFTUP,x,y,0,0)
    SetCursorPos((mX,mY))

def clickButton(WindowTop,WindowLeft,ButtonOffset):
    clickMouse(x,y)

def getWindowFromName(name):
    return wui.FindWindow(None,name)

#offsets always reported in x,y
SNAPSHOT_OFFSET_LB=120,35



def takeScreenCap():
    #wintv=wig.FindWindow(None,"WinTV7")
    wintv=wui.FindWindow(None,"WinTV7")
    if not wintv:
        raise IOError('WinTV7 not found! Is it on!?')
    lb=getLeftBottom(wintv)
    lo=SNAPSHOT_OFFSET_LB[0]
    bo=SNAPSHOT_OFFSET_LB[1]
    x=lb[0]+lo
    y=lb[1]+bo
    clickMouse(x,y,.001) #MAKE SURE THE WINDOW IS NOT COVERED!

def main():
    print(PCLAMP_BUTTON_OFFSETS)
    for x,y in PCLAMP_BUTTON_OFFSETS.values():
        x=x+100
        y=y+100
        clickMouse(x,y,slp=1)


if __name__ == '__main__':
    main()


