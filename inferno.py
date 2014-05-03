#!/usr/bin/env python3.3
""" For Dante
Usage:
    inferno.py <HS1_cell_id> <HS2_cell_id> <HS3_cell_id> <HS4_cell_id> <protocol_id> [ --filepath=<path> ]
    inferno.py --makecsv=<source> <output>
    inferno.py --help
Options:
    -h --help                   print this
    -f --filepath=<path>        set which csv file to write to, IF NONE IT WILL USE HARDCODED FILE
"""


#may not even need rigioman if we can just load in clx and mcc dll handlers from a script, all we need is the filename and the cell ids

from docopt import docopt
args=docopt(__doc__) #do this early to prevent all the lags
print(args)

import os
import pickle
import numpy as np
from mcc import mccControl
from functions import mccFuncs
from gui import getClampexWinName, clickProtocol, clickRecord

#todo all multiclamps

class danteFuncs(mccFuncs):
    ###
    ### Put your functions below! see rig/functions.py for reference specifically mccFuncs and clxFuncs
    ###
    def uidSetMode(self,uid,mode):
        self.mcc.selectUniqueID(uid)
        self.mcc.SetMode(mode)

    def writeData(self):
        ''' This is the function that writes the data we got to file '''
        #TODO format for this

        #write to binary file, full mcc states, functions to get that back out to a csv

        return None

    def printData(self):
        print()
        for line in lines:
            print(line)
    def click_protocol_button(self,button=None):
        pass

    def click_record(self):
        pass




    def DOALLTHETHINGS(hsToCellDict,csvPath): #FIXME eh, given the structure of this program, just stuff these in at init
        stuff=None
        writeFile(csvPath)
        print(csvPath,hsToCellDict)
        #FIXME may need a way to stop execution in the middle???


        #set the mode for each headstage NOTHING ELSE
        #load protocol <- use the mouse click
        #wait for key input or cancel
        #record mcc state, protocol, and cell asociations
        #run protocol <- use the mouse click
        #get the new filename
        #print text to terminal

        hsdict={
            'labels':['gen from output format?'],
            1:{'cell id':'aa',}
        }
        return None


def makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT):
    modeDefs={'v':0,'i':1,'iez':2} #FIXME move this somwehre visible
    modeTup=PROTOCOL_MODE_DICT[ protocolNumber ]
    modes=[ modeDefs[modeName] for modeName in modeTup ]
    uidModeDict={}
    for i in range(len(modes)):
        uid = HS_TO_UID_DICT[ i+1 ] 
        uidModeDict[ uid ] = modes[ i ] #the tuple is just listed headstages 1 through 4 though it could be n now
    return uidModeDict

def makeHeadstageStateDict(uidStateDict):
    hsStateDict={}
    for uid,state in uidStateDict.item():
        hsStateDict[ UID_TO_HS_DICT[uid] ] = state
    return hsStateDict

def addCellToHeadStage(hsToCellDict,hsStateDict): #note this is an in place modification
    for hs,cell in hsToCellDict:
        hsStateDict[hs]['Cell']=cell

def setModes(protocolNumber,mcc): #FIXME this is ugly...
    uidModeDict=makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT)
    for uid,mode in uidModeDict.items():
        mcc.selectUniqueID(uid)
        mcc.SetMode(mode)

def setMCCLoadProt(protocolNumber,mcc):
    setModes(protocolNumber,mcc)
    clickProtocol(protocolNumber)

def getPclampFilename():
    """ YYYY_MM_DD_NNNN.abf """ 
    name=getPclampWinName()
    print(name)
    name=name[-19:]
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
        if not os.isfile(PATH):
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
    from config import MCC_DLLPATH
    from config import HS_TO_UID_DICT
    from config import PROTOCOL_MODE_DICT
    from config import CSVPATH
    from config import PICKPATH
    from config import ROW_ORDER

    checkPath(PICKLEPATH)
    checkPath(CSVPATH)

    #define our constants
    #set variables from the command line
    CSVPATH=args['--filepath']
    protcolNumber = int(args['<protocol_id>'])
    hsToCellDict = {
        1:args['<HS1_cell_id>'],
        2:args['<HS2_cell_id>'],
        3:args['<HS3_cell_id>'],
        4:args['<HS4_cell_id>'],
    }

    #initialize the controllers and the 
    mcc=mccControl(MCC_DLLPATH)


    #set the modes for each headstage and load the protocol
    setMCCLoadProt(protocolNumber,mcc)

    #save the state of each headstage and which cell is associated with it
    uidStateDict=mcc.getMCCState()

    hsStateDict = makeHeadstageStateDict(uidStateDict) #this is our data

    addCellToHeadStage(hsToCellDict,hsStateDict)

    #run pclamp
    clickRecord()

    #get the filename from the windown name! tada! wat a stuipd hack
    sleep(.1) #give the window time to change
    filename = getPclampFilename()

    #save and display everything
    data = { filename : ( protocolNumber , hsStateDict  ) } #INTO THE PICKLE
    pickleIt(data,PICKLEPATH)
    textData = makeText( data )
    updateCSV(textData.replace('\t',',')
    print(textData) 

    


if __name__ == '__main__':
    main()

