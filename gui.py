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
    BUTTON_WIDTH=28
    G0_START=68
    G1_START=305
    G2_START=400
    G3_START=495
    #number of buttons per group
    G0_COUNT=8
    G1_COUNT=3
    G2_COUNT=3
    G3_COUNT=3

    g0={ 1+n:( G0_START + BUTTON_WIDTH * n , PROT_Y_OFFSET) for n in range(G0_COUNT) }
    g1={ 1+n+G0_COUNT:( G1_START + BUTTON_WIDTH * n , PROT_Y_OFFSET) for n in range(G1_COUNT) }

    g2={ 1+n+G0_COUNT+G1_COUNT:( G2_START + BUTTON_WIDTH * n , PROT_Y_OFFSET) for n in range(G2_COUNT) }
    g3={ 1+n+G0_COUNT+G1_COUNT+G2_COUNT:( G3_START + BUTTON_WIDTH * n , PROT_Y_OFFSET) for n in range(G3_COUNT) }

    offsetDict={ 'record':(350,65) }
    offsetDict.update(g0)
    offsetDict.update(g1)
    offsetDict.update(g2)
    offsetDict.update(g3)
    return offsetDict

PCLAMP_BUTTON_OFFSETS = make_offsets()


def getWindows():
    """ Get a list of all the windows. List of tuples (int, string)
    the string is the window name. """
    toplist=[]
    winlist=[]

    def enum_callback(hwnd, results):
        winlist.append((hwnd,wig.GetWindowText(hwnd)))

    wig.EnumWindows(enum_callback, toplist)

    return winlist

def getClampexWinName():
    for i,name in getWindows():
        if name.count('Clampex'):
            return name
 
def getWindowFromName(name):
    print(name)
    return wui.FindWindow(None,name)

def getLeftBottom(window):
    return window.GetWindowRect()[0::3] #left,top,right,bottom

def getLeftTop(window):
    return window.GetWindowRect()[:2]
     
def getClampexWinLeftTop():
    name=getClampexWinName()
    window=getWindowFromName(name)
    return getLeftTop(window)

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

def clickProtocol(protocolNumber):
    leftTop=getClampexWinLeftTop()
    offset=PCLAMP_BUTTON_OFFSETS[protocolNumber]
    clickButton(leftTop,offset)

def clickRecord():
    leftTop=getClampexWinLeftTop()
    offset=PCLAMP_BUTTON_OFFSETS['record']
    clickButton(leftTop,offset)


def main():
    print(PCLAMP_BUTTON_OFFSETS)
    left,top = getClampexWinLeftTop()
    for x,y in PCLAMP_BUTTON_OFFSETS.values():
        x=x+left
        y=y+top
        clickMouse(x,y,1)


if __name__ == '__main__':
    main()


