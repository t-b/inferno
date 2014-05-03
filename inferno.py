#!/usr/bin/env python3.3
""" For Dante
Usage:
    inferno.py <HS1_cell_id> <HS2_cell_id> <HS3_cell_id> <HS4_cell_id> <protocol_id> [ --filepath=<path> ]
    inferno.py --makecsv=<pickle> <output>
    inferno.py --help
Options:
    -h --help                   print this
    -f --filepath=<path>        set which csv file to write to, IF NONE IT WILL USE HARDCODED FILE
"""

from docopt import docopt
args=docopt(__doc__) #do this early to prevent all the lags
print(args)

import os
import pickle
from time import sleep
from mcc import mccControl
from functions import mccFuncs
from gui import getPclampWinName, clickProtocol, clickRecord

#set the mode for each headstage NOTHING ELSE
#load protocol <- use the mouse click
#wait for key input or cancel
#record mcc state, protocol, and cell asociations
#run protocol <- use the mouse click
#get the new filename
#print text to terminal

def makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT):
    modeDefs={'v':0,'i':1,'iez':2} #FIXME move this somwehre visible
    modeTup=PROTOCOL_MODE_DICT[ protocolNumber ]
    modes=[ modeDefs[modeName] for modeName in modeTup ]
    uidModeDict={}
    for i in range(len(modes)-1):
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

def setMCCLoadProt(uidModeDict,protocolNumber,mcc):
    setModes(uidModeDict,mcc)
    clickProtocol(protocolNumber)

def getPclampFilename():
    """ YYYY_MM_DD_NNNN.abf """ 
    name=getPclampWinName()
    if name is None:
        raise IOError('pCLAMP is not on!')
    print(name)
    name=name[11:30] #FIXME should not hardcode this, also first run may not have full 30...
    print(name)
    return name

def rowPrintLogic(row,StateDict): #FIXME UNITS!!!
    if row == 'Holding':
        if StateDict['HoldingEnable']:
            out = StateDict[row]
        else:
            out = 'OFF'
    elif row == 'BridgeBalResist':
        if StateDict['BridgeBalEnable']:
            out = StateDict[row]
        else:
            out = 'OFF'
    else:
        out = StateDict[row]

    return out

def makeText(data,ROW_ORDER,delimiter='\t'):
    # for reference: { filename : ( protocolNumber , hsStateDict  ) }
    lines=[]
    lines.append( delimiter.join( ('','HS1','HS2','HS3','HS4') ) )
    for filename , ( protocolNumber , hsStateDict ) in data.items():

        trialNumber=filename[-7:-3]
        lines.append( delimiter.join( (trialNumber , protocolNumber ,'','','') ) )

        for row in ROW_ORDER:
            values=[row]
            for i in range(1,5):
                values.append( rowPrintLogic( row,hsStateDict[i] ) )

            lines.append( delimiter.join(values) )
    return '\n'.join(lines)

#output format

#filename format YYYY_MM_DD_nnnn
#protocol p1 p2 p3 p4 corrisponding to the buttons

#Trial nnnn p1
#headstage  1   2   3   4
#cell id    a   b   c   d 
#mode       vc  ic  vc  ic #map between mcc + channel and the digitizer input channel
#holding    -70 OFF OFF -70 #OFF for holding disabled
#bridge balance

#structure for associating protocols to mcc settings

def checkPath(PATH):
    if os.path.exists(PATH):
        if not os.path.isfile(PATH):
             raise IOError( 'Path is not a file!' )
        else:
            return None
    else:
        return None

def openPickle(PICKLEPATH):
    f = open(PICKLEPATH, 'rb')
    saved_data = pickle.load(f)
    f.close()
    return saved_data

def pickleIt(data,PICKLEPATH):
    """" ALWAYS CHECK FOR PICKLEPATH FIRST!!!! """

    if os.path.exists(PICKLEPATH):
        saved_data = openPickle(PICKLEPATH)
    else:
        saved_data = {}

    saved_data.update(data)
    f = open(PICKLEPATH, 'xb') #FIXME is there a way to NOT thrash the disk AND risk data loss?
    pickle.dump( saved_data , f )
    f.close()


def updateCSV(textData,CSVPATH):
    if os.path.exists(CSVPATH):
        f = open( CSVPATH , 'wt' )
    else:
        f = open( CSVPATH , 'xt' )
    f.write(textData)
    f.close()

def main():
    #see if pclamp is on and get the old filename for error checking on the new filename
    old_filename = getPclampFilename()
    
    #import and check config settings
    from config import PICKLEPATH

    CSVPATH=args['--filepath']
    if not CSVPATH:
        from config import CSVPATH

    checkPath(PICKLEPATH)
    checkPath(CSVPATH)

    from config import MCC_DLLPATH
    from config import HS_TO_UID_DICT
    from config import PROTOCOL_MODE_DICT
    from config import ROW_ORDER

    UID_TO_HS_DICT= { v:k for k,v in HS_TO_UID_DICT.items() }

    #set variables from the command line
    protocolNumber = int(args['<protocol_id>'])
    hsToCellDict = {
        1:args['<HS1_cell_id>'],
        2:args['<HS2_cell_id>'],
        3:args['<HS3_cell_id>'],
        4:args['<HS4_cell_id>'],
    }


    #initialize the controller
    mcc=mccControl(MCC_DLLPATH)
    mccF=mccFuncs(mcc)

    #make the mode dict for the headstages
    uidModeDict=makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT)


    #set the modes for each headstage and load the protocol
    setMCCLoadProt(uidModeDict,protocolNumber,mcc)

    #save the state of each headstage and which cell is associated with it
    uidStateDict=mccF.getMCCState()
    mccF.cleanup() #make sure we get rid of the dllhandels

    hsStateDict = makeHeadstageStateDict(uidStateDict,UID_TO_HS_DICT) #this is our data

    addCellToHeadStage(hsToCellDict,hsStateDict)
    
    print(hsStateDict)

    #run pclamp
    clickRecord()

    #get the filename from the windown name! tada! wat a stuipd hack
    sleep(.1) #give the window time to change
    filename = getPclampFilename()

    #TODO deal with fact that filename wont change if you stop the recording
    #assert filename != old_filename, 'Warning! filename has not changed! Something is wrong!'

    #save and display everything
    data = { filename : ( protocolNumber , hsStateDict  ) } #INTO THE PICKLE
    pickleIt(data,PICKLEPATH)
    textData = makeText( data , ROW_ORDER )
    updateCSV( textData.replace('\t',',') , CSVPATH )
    print(textData) 


if __name__ == '__main__':
    main()

