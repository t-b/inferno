from time import sleep
from gui import getWindows, getWindowFromName, getLeftTop, clickButton
 
#empirically determined offsets from the top left corner of the clampex window
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

CLAMPEX_BUTTON_OFFSETS = make_offsets()


def ClampexLoadProtocol(protocolNumber):
    leftTop=getClampexWinLeftTop()
    offset=CLAMPEX_BUTTON_OFFSETS[protocolNumber]
    clickButton(leftTop,offset)

def ClampexRecord():
    leftTop=getClampexWinLeftTop()
    offset=CLAMPEX_BUTTON_OFFSETS['record']
    clickButton(leftTop,offset)
    sleep(.1) #there is a weird bug where another window pops up and can sometimes block the first click, so click twice
    clickButton(leftTop,offset)

def ClampexGetFilename():
    """ YYYY_MM_DD_NNNN.abf """ 
    sleep(.1) #give the window time to change
    name=getClampexWinName()
    if name is None:
        raise IOError('Clampex is not on!')
    print(name)
    name=name.replace('[','')
    print(name)
    name=name[10:29] #FIXME should not hardcode this, also first run may not have full 30...
    print(name)
    return name

def getClampexWinName():
    for i,name in getWindows():
        if name.count('Clampex'):
            return name

def getClampexWinLeftTop():
    name=getClampexWinName()
    window=getWindowFromName(name)
    return getLeftTop(window)

def main():
    print(CLAMPEX_BUTTON_OFFSETS)
    for offset in CLAMPEX_BUTTON_OFFSETS.values():
        clickButton((0,0),offset)

if __name__ == '__main__':
    main()
