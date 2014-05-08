#!/usr/bin/env python3.3
"""Inferno: electrophysiology with Clampex in a shell.
Usage:
    inferno.py run <HSn_cell_id>... [ --protocol=<id> --config=<path> --csvpath=<path> ]
    inferno.py makecsv [ <pickle> [ <output> ] ] [ --config=<path> ]
    inferno.py --help

Options:
    -h --help           print this
    -p --protocol=<id>  set which protocol to load, if not set will run with current settings
    -f --csvpath=<path> set which csv file to write, defaults to CSVPATH from config
    -c --config=<path>  set which config file to use [default: config.ini]
""" #FIXME why does the repeating argument need to come last in this instance :(

import sys

from docopt import docopt
args=docopt(__doc__)
#print(args)

from time import sleep
from mcc import mccControl
from functions import mccFuncs

from config import parseConfig

from funcs import getClampexFilename
from funcs import makeUIDModeDict
from funcs import setMCCLoadProt
from funcs import clickProtocol
from funcs import makeHeadstageStateDict
from funcs import addCellToHeadStage
from funcs import clickRecord

from output import makeText

from dataio import dataio

def main():
    #enter make csv mode?
    if args['makecsv']:
        print('making csv from binary data!')
        configTuple = parseConfig(args['--config'])
        PICKLEPATH, CSVPATH, MCC_DLLPATH, NO_CELL_STRING, OFF_STRING, ROW_ORDER, ROW_NAMES, HS_TO_UID_DICT, PROTOCOL_MODE_DICT, STATE_TO_UNIT_DICT = configTuple
        if args['<pickle>'] is not None:
            PICKLEPATH = args['<pickle>']
        if args['<output>'] is not None:
            CSVPATH = args['<output>']
        with dataio(PICKLEPATH,CSVPATH) as dataman:
            data=dataman.loadPickle()
        nHeadstages = len(HS_TO_UID_DICT)
        textData = makeText( data , ROW_ORDER, ROW_NAMES , OFF_STRING , STATE_TO_UNIT_DICT, nHeadstages )
        csvData = makeText( data , ROW_ORDER, ROW_NAMES, OFF_STRING, STATE_TO_UNIT_DICT, nHeadstages, ',' )
        print(textData)
        dataman.writeCSV(csvData)
        return None

    #import and check config settings
    configTuple = parseConfig(args['--config'])
    PICKLEPATH, CSVPATH, MCC_DLLPATH, NO_CELL_STRING, OFF_STRING, ROW_ORDER, ROW_NAMES, HS_TO_UID_DICT, PROTOCOL_MODE_DICT, STATE_TO_UNIT_DICT = configTuple
    if args['--csvpath']:
        CSVPATH = args['--csvpath']

    #see if clampex is on
    old_filename = getClampexFilename()

    #set variables from the command line
    cell_list=args['<HSn_cell_id>']
    hsToCellDict = { n+1:cell_list[n] for n in range(len(cell_list)) }
    #print(hsToCellDict)

    #get the total number of headstages for formatting
    nHeadstages = len(HS_TO_UID_DICT)

    UID_TO_HS_DICT= { v:k for k,v in HS_TO_UID_DICT.items() }

    #initialize the controller
    with mccControl(MCC_DLLPATH) as mcc:
        for uid in UID_TO_HS_DICT:
            try:
                mcc.mcDict[uid]
            except KeyError:
                print(mcc.mcDict.keys())
                raise IOError('MultiClamp %s is not on! Exiting.'%uid)

        mccF=mccFuncs(mcc)

        #open the csv and pickle, make sure they are valid and keep a lock on them
        #needs to happen before we touch any of the settings on the mcc etc so gurantee a save
        with dataio(PICKLEPATH,CSVPATH) as dataman:

            if args['--protocol'] is not None:
                protocolNumber = int(args['--protocol'])

                #make the mode dict for the headstages
                uidModeDict=makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT)

                #set the modes for each headstage and load the protocol
                setMCCLoadProt(uidModeDict,protocolNumber,mcc)

            else:
                protocolNumber = 'prev' #FIXME DAMN IT

            #after setting all headstages drop the headstages we do not need from saving
            for hs in range(1,nHeadstages+1):
                try:
                    if hsToCellDict[hs] == NO_CELL_STRING:
                        HS_TO_UID_DICT.pop(hs) #pop hs that we specify with no cell
                except KeyError:
                    if hs <= nHeadstages: #pop hs not on cmd line
                        HS_TO_UID_DICT.pop(hs)

            UID_TO_HS_DICT= { v:k for k,v in HS_TO_UID_DICT.items() }

            #save the state of each headstage and which cell is associated with it
            uidStateDict=mccF.getMCCState(UID_TO_HS_DICT) #give it the uids in the form of keys type magic

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
            textData = makeText( data , ROW_ORDER, ROW_NAMES , OFF_STRING , STATE_TO_UNIT_DICT, nHeadstages )
            csvData = makeText( data , ROW_ORDER, ROW_NAMES, OFF_STRING, STATE_TO_UNIT_DICT, nHeadstages, ',' )
            dataman.updateCSV( csvData )
    print(textData) 


if __name__ == '__main__':
    main()

