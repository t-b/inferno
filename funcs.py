""" RENAME THIS FILE ONCE WE FIX functions.py and that damned class...
    This file holds all the functions we use to make inferno.py work.
    This will simplify testing.
"""

from time import sleep
from gui import getWindows, getWindowFromName, getTopLeft, clickButton
 
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

     
def getClampexWinLeftTop():
    name=getClampexWinName()
    window=getWindowFromName(name)
    return getLeftTop(window)


def makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT):
    modeDefs = { v:k for k,v in MCC_MODE_DICT.items() }
    modeTup=PROTOCOL_MODE_DICT[ protocolNumber ]
    modes=[ modeDefs[modeName] for modeName in modeTup ]
    uidModeDict={}
    for i in range(len(modes)):
        uid = HS_TO_UID_DICT[ i+1 ]
        uidModeDict[ uid ] = modes[ i ] #the tuple is just listed headstages 1 through 4 though it could be n now
    return uidModeDict

def makeHeadstageStateDict(uidStateDict, UID_TO_HS_DICT):
    hsStateDict={}
    for uid,state in uidStateDict.items():
        hsStateDict[ UID_TO_HS_DICT[uid] ] = state
    return hsStateDict

def addCellToHeadStage(hsToCellDict,hsStateDict): #note this is an in place modification
    for hs,cell in hsToCellDict.items():
        hsStateDict[hs]['Cell']=cell

def setModes(uidModeDict,mcc): #FIXME this is ugly...
    for uid,mode in uidModeDict.items():
        mcc.selectUniqueID(uid)
        mcc.SetMode(mode)
    sleep(1) #it takes about 1 second for MCC to update and the telegraph inputs to change

def setMCCLoadProt(uidModeDict,protocolNumber,mcc):
    setModes(uidModeDict,mcc)
    clickProtocol(protocolNumber)

def getClampexFilename():
    """ YYYY_MM_DD_NNNN.abf """ 
    def getClampexWinName()
        for i,name in getWindows():
            if name.count('Clampex'):
                return name
    name=getClampexWinName()
    if name is None:
        raise IOError('pCLAMP is not on!')
    #print(name)
    name=name[11:30] #FIXME should not hardcode this, also first run may not have full 30...
    #print(name)
    return name

def rowPrintLogic(row,StateDict,delim,OFF_STRING): #FIXME UNITS!!!
    if row == 'Holding':
        if StateDict['HoldingEnable']:
            out = StateDict[row]
            if delim=='\t':
                out='%2.2f'%out
        else:
            out = OFF_STRING
    elif row == 'BridgeBalResist':
        if StateDict['BridgeBalEnable'] and StateDict['Mode'] == 1:
            out = StateDict[row]
            if delim=='\t':
                out='%1.1e'%out
        else:
            out = OFF_STRING
    elif row == 'Mode':
        out = MCC_MODE_DICT[ StateDict[row] ]
    else:
        out = StateDict[row]

    return out

def makeText(data,ROW_ORDER,ROW_NAMES,OFF_STRING,delimiter='\t'):
    # for reference: data = { filename : ( protocolNumber , hsStateDict  ) }
    lines=[]

    numberHeadstages=len(list(data.values())[0][1]) #FIXME doesnt work if we change the number of headstages half way through? but I guess we could just list n headstages
    lineOneList=['HS%s'%n * (n>0) for n in range(numberHeadstages+1)]
    lines.append( '\n'+delimiter.join( lineOneList ) ) #\n is to make it place nice with .split('\n',1)[1] or append the HS line on a new line every time

    for filename , ( protocolNumber , hsStateDict ) in data.items():

        trialNumber=filename[-8:-4]
        lines.append( delimiter.join( ('%s'%trialNumber , '%s'%protocolNumber ,'','','') ) )

        for row in ROW_ORDER:
            values=[ ROW_NAMES[row] ]
            for i in range(1,5):
                values.append( '%s'%rowPrintLogic( row,hsStateDict[i],delimiter,OFF_STRING ) )

            lines.append( delimiter.join(values) )
    return '\n'.join(lines)

    #output format

    #filename format YYYY_MM_DD_nnnn
    #protocol p1 p2 p3 p4 corrisponding to the buttons

    #nnnn   p1
    #       1   2   3   4
    #cell   a   b   c   d 
    #mode   vc  ic  vc  ic #map between mcc + channel and the digitizer input channel
    #holding    -70 OFF OFF -70 #OFF for holding disabled
    #bridge balance

#structure for associating protocols to mcc settings
def main():
    print(PCLAMP_BUTTON_OFFSETS)
    for offset in PCLAMP_BUTTON_OFFSETS.values()
        clickButton(getClampexWinLeftTop(),offset)

if __name__ == '__main__':
    main()
