""" RENAME THIS FILE ONCE WE FIX functions.py and that damned class...
    This file holds all the functions we use to make inferno.py work.
    This will simplify testing.
"""

from time import sleep
from mcc import MCC_MODE_DICT
from gui import getWindows, getWindowFromName, getLeftTop, clickButton
 
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


def clickProtocol(protocolNumber):
    leftTop=getClampexWinLeftTop()
    offset=PCLAMP_BUTTON_OFFSETS[protocolNumber]
    clickButton(leftTop,offset)

def clickRecord():
    leftTop=getClampexWinLeftTop()
    offset=PCLAMP_BUTTON_OFFSETS['record']
    clickButton(leftTop,offset)

def getClampexWinName():
    for i,name in getWindows():
        if name.count('Clampex'):
            return name

def getClampexWinLeftTop():
    name=getClampexWinName()
    window=getWindowFromName(name)
    return getLeftTop(window)

def makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT):
    modeDefs = { v:k for k,v in MCC_MODE_DICT.items() }
    modeTup=PROTOCOL_MODE_DICT[ protocolNumber ]
    modes=[ modeDefs[modeName] if modeName in modeDefs else None for modeName in modeTup ]
    print(modes)
    uidModeDict={}
    #this only sets the headstages that have cells
    for headstage,uid in HS_TO_UID_DICT.items():
        uidModeDict[ uid ] = modes[ headstage - 1 ]
    return uidModeDict

def makeHeadstageStateDict(uidStateDict, UID_TO_HS_DICT):
    hsStateDict={}
    for uid,headstage in UID_TO_HS_DICT.items():
        hsStateDict[ headstage ] = uidStateDict[uid]
    return hsStateDict

def addCellToHeadStage(hsToCellDict,hsStateDict): #note this is an in place modification
    #if we iterate through hsToCellDict xx is still there
    for headstage,stateDict in hsStateDict.items():
        #try: #fairly certain this is no longer needed
        stateDict['Cell'] = hsToCellDict[headstage]
        #except KeyError: 
            #print('Cell %s was not added because you do not have that many headstages!'%cell)

def setModes(uidModeDict,mcc): #FIXME this is ugly...
    for uid,mode in uidModeDict.items():
        if mode is None: #this works with makeUIDModeDict
            continue
        mcc.selectUniqueID(uid)
        mcc.SetMode(mode)
    sleep(1) #it takes about 1 second for MCC to update and the telegraph inputs to change

def setMCCLoadProt(uidModeDict,protocolNumber,mcc):
    setModes(uidModeDict,mcc)
    clickProtocol(protocolNumber)

def getClampexFilename():
    """ YYYY_MM_DD_NNNN.abf """ 
    name=getClampexWinName()
    if name is None:
        raise IOError('pCLAMP is not on!')
    #print(name)
    name=name[11:30] #FIXME should not hardcode this, also first run may not have full 30...
    #print(name)
    return name

def main():
    print(PCLAMP_BUTTON_OFFSETS)
    for offset in PCLAMP_BUTTON_OFFSETS.values():
        #clickButton(getClampexWinLeftTop(),offset)
        clickButton((0,0),offset)

if __name__ == '__main__':
    main()
