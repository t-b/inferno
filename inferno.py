#!/usr/bin/env python3.3
""" For Dante
Usage:
    inferno.py <HS1_cell_id> <HS2_cell_id> <HS3_cell_id> <HS4_cell_id> <protocol_id> [ --filepath=<path> ]
    inferno.py -h | --help
Options:
    -h --help                   print this
    -f --filepath=<path>        set which csv file to write to, IF NONE IT WILL USE HARDCODED FILE
"""


#may not even need rigioman if we can just load in clx and mcc dll handlers from a script, all we need is the filename and the cell ids

from docopt import docopt
args=docopt(__doc__) #do this early to prevent all the lags
print(args)

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

def appendTrailToPickle(trialDict):
    return 0

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
    uidModeDict=makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT):
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

def makeTextFile(filenameToExperimentTuple,rowOrdering):
    lines=[]
    linebase='%s\t%s\t%s\t%s\t%s'
    lines.append( linebase%('','HS1','HS2','HS3','HS4') )
    for filename,(protocolNumber,headstageStateDict) in filenameToExperimentDict.items():
        trialNumber=filename[-7:-3]

        lines.append( linbebase%(trialNumber,protocolNumber,'','','') )

        for cell_id, stateDict in experimentDict.items():
            lines.append(
                      linebase%('cell',1,2,3,4)
            )

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





def main():
    from config import HS_TO_UID_DICT
    from config import MCC_DLLPATH
    from config import PROTOCOL_MODE_DICT

    #define our constants
    #set variables from the command line
    csvPath=args['--filepath']
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

    filenameToExperimentTuple={} #this goes in the pickle 
    { filename : ( protocolNumber , hsStateDict  ) }

    row_ordering=['Cell','Mode','Holding','BridgeBalResist']
    


if __name__ == '__main__':
    main()

