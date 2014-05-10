""" 
    This file holds the functions that make inferno work that are associated
    with MultiClampCommander and assigning cells to headstages.
"""
from time import sleep
from mcc import MCC_MODE_DICT

def makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT):
    try: 
        modeTup = PROTOCOL_MODE_DICT[ protocolNumber ]
    except KeyError:
        return None
    modeDefs = { v:k for k,v in MCC_MODE_DICT.items() }
    modes = [ modeDefs[ modeName ] if modeName in modeDefs else None for modeName in modeTup ]
    uidModeDict = {}
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
            #pass #this will just ignore headstages between m and n where m is the number of cells specified on the command line and n is the number of headstages
        #we have to handle going over vs going under one way or another this seems ok, maybe going over is rarer so we should flip which dict we iterate through, but no need for now

def MCCsetModes(uidModeDict,mcc): #FIXME this is ugly...
    for uid,mode in uidModeDict.items():
        if mode is None: #this works with makeUIDModeDict
            continue
        mcc.selectUniqueID(uid)
        mcc.SetMode(mode)
    sleep(1) #it takes about 1 second for MCC to update and the telegraph inputs to change

if __name__ == '__main__':
    main()
