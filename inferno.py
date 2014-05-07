#!/usr/bin/env python3.3
"""Inferno: electrophysiology with Clampex in a nutshell.
Usage:
    inferno.py <protocol_id> <HS_cell_id>... [ --config=<path> --csvpath=<path> ] 
    inferno.py makecsv [ <pickle> [ <output> ] ]
    inferno.py --help

Options:
    -h --help                   print this
    -f --csvpath=<path>         set which csv file to write to, IF NONE IT WILL USE HARDCODED FILE
    -c --config=<path>          set which config file to use [default: config.ini]
""" #FIXME why does the repeating argument need to come last in this instance :(

from docopt import docopt
args=docopt(__doc__) #do this early to prevent all the lags
print(args)

from time import sleep
from mcc import mccControl
from functions import mccFuncs

from cfg import parseConfig

from funcs import getClampexFilename
from funcs import makeUIDModeDict
from funcs import setMCCLoadProt
from funcs import clickProtocol
from funcs import makeHeadstageStateDict
from funcs import addCellToHeadStage
from funcs import clickRecord

from output import makeText

from dataio import dataio


def loadConfig():
    """ loads in all the data from the config file, this way you can have
    multiple configs, or save your old configs """

    #TODO
    #make sure that len(value) in PROTOCOL_MODE_DICT matches
    #len(HS_TO_UID_DICT)

def main():
    #enter make csv mode?
    if args['makecsv']:
        print('making csv from binary data!')
        print(args['<pickle>'])
        print(args['<output>'])
        return None

    #import and check config settings
    configTuple = parseConfig(args['--config'])
    PICKLEPATH, CSVPATH, MCC_DLLPATH, OFF_STRING, ROW_ORDER, ROW_NAMES, HS_TO_UID_DICT, PROTOCOL_MODE_DICT, MODE_TO_UNIT_DICT, STATE_TO_UNIT_DICT = configTuple
    print(configTuple)
    if args['--csvpath']:
        CSVPATH = args['--csvpath']

    #see if clampex is on, get the old filename (error check?)
    old_filename = getClampexFilename()

    #open the csv and pickle, make sure they are valid and keep a lock on them
    with dataio(PICKLEPATH,CSVPATH) as dataman:

        UID_TO_HS_DICT= { v:k for k,v in HS_TO_UID_DICT.items() }

        #set variables from the command line
        protocolNumber = int(args['<protocol_id>'])
        try: 
            hsToCellDict = {
                1:args['<HS1_cell_id>'],
                2:args['<HS2_cell_id>'],
                3:args['<HS3_cell_id>'],
                4:args['<HS4_cell_id>'],
            }
        except KeyError: #testing the <>... format
            cell_list=args['<HS_cell_id>']
            hsToCellDict = { n+1:cell_list[n] for n in range(len(cell_list)) }


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
        textData = makeText( data , ROW_ORDER, ROW_NAMES , OFF_STRING , STATE_TO_UNIT_DICT, MODE_TO_UNIT_DICT )
        csvData = makeText( data , ROW_ORDER, ROW_NAMES, OFF_STRING, STATE_TO_UNIT_DICT, MODE_TO_UNIT_DICT, ',' )
        dataman.updateCSV( csvData )
        print(textData) 


if __name__ == '__main__':
    main()

