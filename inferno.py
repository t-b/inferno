#!/usr/bin/env python3.3
""" For Dante
Usage:
    inferno.py <HS1_cell_id> <HS2_cell_id> <HS3_cell_id> <HS4_cell_id> <protocol_id> [ --filepath=<path> --config=<path> ] 
    inferno.py makecsv [ <pickle> [ <output> ] ]
    inferno.py --help
Options:
    -h --help                   print this
    -f --filepath=<path>        set which csv file to write to, IF NONE IT WILL USE HARDCODED FILE
    -c --config=<path>          select a config.py file other than default
"""

from docopt import docopt
args=docopt(__doc__,options_first=True) #do this early to prevent all the lags
#print(args)

from time import sleep
from mcc import mccControl
from functions import mccFuncs

from funcs import getClampexFilename
from funcs import makeUIDModeDict
from funcs import setMCCLoadProt
from funcs import clickProtocol
from funcs import makeHeadstageStateDict
from funcs import addCellToHeadStage
from funcs import clickRecord
from funcs import makeText

from dataio import dataio


def loadConfig():
    """ loads in all the data from the config file, this way you can have
    multiple configs, or save your old configs """
    #TODO
    #make sure that len(value) in PROTOCOL_MODE_DICT matches
    #len(HS_TO_UID_DICT)

def main():
    if args['makecsv']:
        print('making csv from binary data!')
        print(args['<pickle>'])
        print(args['<output>'])
        return None

    #see if pclamp is on and get the old filename for error checking on the new filename
    old_filename = getClampexFilename()
    
    #import and check config settings
    from config import PICKLEPATH

    CSVPATH=args['--filepath']
    if not CSVPATH:
        from config import CSVPATH

    dataman=dataio(PICKLEPATH,CSVPATH) #open the csv and pickle

    from config import MCC_DLLPATH
    from config import HS_TO_UID_DICT
    from config import PROTOCOL_MODE_DICT
    from config import ROW_ORDER
    from config import ROW_NAMES
    from config import OFF_STRING

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
    
    #print(hsStateDict)

    #run pclamp
    clickRecord()

    #get the filename from the windown name! tada! wat a stuipd hack
    sleep(.1) #give the window time to change
    filename = getClampexFilename()

    #TODO deal with fact that filename wont change if you stop the recording
    #assert filename != old_filename, 'Warning! filename has not changed! Something is wrong!'

    #save and display everything
    data = { filename : ( protocolNumber , hsStateDict  ) } #INTO THE PICKLE
    dataman.updatePickle(data)
    textData = makeText( data , ROW_ORDER, ROW_NAMES , OFF_STRING )
    csvData = makeText( data , ROW_ORDER, ROW_NAMES, OFF_STRING, ',' )
    dataman.updateCSV( csvData )
    print(textData) 
    dataman.cleanup()


if __name__ == '__main__':
    main()

