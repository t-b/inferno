#!/usr/bin/env python3.3
""" For Dante
Usage:
    inferno.py <HS1_id> <HS2_id> <HS3_id> <HS4_id> <Protocol_id> [ --filepath=<path> ]
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
from gui import *
from config import SERIAL_TO_HS_DICT

#todo all multiclamps

class danteFuncs(mccFuncs):
    def __init__(self,mcc,csvFile,hsToCellDict):
        """ Some voodoo to get everything up and running without fixing other code """
        super().__init__(mcc=mcc)
        self.csvFile=csvFile
        self.hsToCellDict=hsToCellDict

    ###
    ### Put your functions below! see rig/functions.py for reference specifically mccFuncs and clxFuncs
    ###

    def writeData(self):
        ''' This is the function that writes the data we got to file '''
        #TODO format for this

        #write to binary file, full mcc states, functions to get that back out to a csv

        return None

    def printData(self):
        print()
        for line in lines:
            print(line)

    def getClampexWinName(self):
        for i,name in get_windows():
            if name.count('Clampex'):
                return name

    def getClampexWindow(self):
        self.cw=getWindowFromName(name)

    def click_protocol_button(self,button=None):
        
    def click_record(self):



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


def formatDataRow(stateDict):
    """ take the data structure and format it for viewing"""
    lines=[ '%s\t%s\t%s\t%s\t%s' ] * 6 #creates a list of 5 empty strings we can format




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
    #define our constants
    mccDllPath=''

    #set variables from the command line
    csvPath=args['--filepath']
    hsToCellDict={ #FIXME somehow this seems redundant...
        1:args['<HS1_id>'],
        2:args['<HS2_id>'],
        3:args['<HS3_id>'],
        4:args['<HS4_id>'],
    }


    #make sure headstage numbers line up correctly!

    #initialize the controllers and the 
    mcc=mccControl(mccDllPath)

    #create an instance of danteFuncs using the controllers, csvFile, and 
    fucntions=danteFuncs(mcc,csvFile,hsToCellDict)

    #run the protocol
    functions.DOALLTHETHIGNS()




if __name__ == '__main__':
    main()

