#!/usr/bin/env python3.3
from __init__ import __version__
from config import DEFAULT_USER_DIR
__doc__ = """

Inferno: electrophysiology with Clampex in a shell.
Usage:
    inferno.py run <HSn_cell_id>... [ --protocol=<id> --config=<path> --csvpath=<path> --stop ]
    inferno.py makecsv [ --csvpath=<path> --pikpath=<path> --config=<path> ]
    inferno.py setup
    inferno.py --help

Options:
    -h --help           print this
    -p --protocol=<id>  set protocol to load, otherwise use current settings
    -c --config=<path>  set config file to use [default: %sconfig.ini]
    -f --csvpath=<path> set csv file to write, default: CSVPATH from config
    -k --pikpath=<path> set pickle file to use, default: PICKLEPATH from config
    -s --stop           stop/pause between loading protocol and recording
    -v --version        show version

"""%DEFAULT_USER_DIR

import sys

from docopt import docopt
args=docopt( __doc__ , version = 'Inferno '+__version__ )
#print(args)

from time import sleep
from mcc import mccControl
from functions import mccFuncs

from config import parseConfig, firstRun

from funcs import makeUIDModeDict
from funcs import makeHeadstageStateDict
from funcs import addCellToHeadStage
from funcs import MCCsetModes

from clampex import ClampexLoadProtocol as LoadProtocol
from clampex import ClampexRecord as Record
from clampex import ClampexGetFilename as GetFilename

from key import GetKey

from output import makeText

from dataio import dataio

def main():
    #import and check config settings
    if firstRun(args['--config']):
        return None
    elif args['setup']:
        print('Setup already complete!')
        return None
    configTuple = parseConfig(args['--config'])
    PICKLEPATH, CSVPATH, MCC_DLLPATH, PAUSE_ON_LOAD, NO_CELL_STRING, OFF_STRING, ROW_ORDER, ROW_NAMES, HS_TO_UID_DICT, PROTOCOL_MODE_DICT, STATE_TO_UNIT_DICT = configTuple

    #get the total number of headstages
    nHeadstages = len(HS_TO_UID_DICT)

    #enter make csv mode?
    if args['makecsv']:
        print('making csv from binary data!')
        if args['--pikpath'] is not None:
            PICKLEPATH = args['--pikpath']
        if args['--csvpath'] is not None:
            CSVPATH = args['--csvpath']
        with dataio(PICKLEPATH,CSVPATH) as dataman:
            data=dataman.loadPickle()
        textData = makeText( data , ROW_ORDER, ROW_NAMES , OFF_STRING , STATE_TO_UNIT_DICT, nHeadstages )
        csvData = makeText( data , ROW_ORDER, ROW_NAMES, OFF_STRING, STATE_TO_UNIT_DICT, nHeadstages, ',' )
        print(textData)
        dataman.writeCSV(csvData)
        return None

    #did we set the csvpath on the commandline?
    if args['--csvpath']:
        CSVPATH = args['--csvpath']

    #see if clampex is on, this is rather a hack and should be made explicit
    old_filename = GetFilename()

    #set variables from the command line
    cell_list=args['<HSn_cell_id>']
    hsToCellDict = { n+1:cell_list[n] for n in range(len(cell_list)) }

    UID_TO_HS_DICT= { v:k for k,v in HS_TO_UID_DICT.items() }

    #seee if we have a protocol
    if args['--protocol'] is not None:
        if type(args['--protocol']) == int:
            protocolNumber = int(args['--protocol'])
        else:
            print( 'Protocol %s is not defined! Exiting.'%args['--protocol'] )
            return None

        #make the mode dict for the headstages
        uidModeDict=makeUIDModeDict(protocolNumber,PROTOCOL_MODE_DICT,HS_TO_UID_DICT)

        if uidModeDict is None:
            print( 'Protocol %s is not defined! Exiting.'%protocolNumber )
            return None
    else:
        protocolNumber = 'prev' #FIXME DAMN IT


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

            #set the modes for each headstage and load the protocol
            if args['--protocol'] is not None:
                MCCsetModes(uidModeDict,mcc)
                LoadProtocol(protocolNumber)
                #FIXME dissociate this to enable modular use


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
            
            #if we need a pause, from command line or from the config...
            if PAUSE_ON_LOAD:
                print('Hit any key to record.')
                GetKey()

            #run  the protocol
            Record()

            #get the filename from the windown name! tada! wat a stuipd hack
            filename = GetFilename()

            #save and display everything
            data = { filename : ( protocolNumber , hsStateDict  ) } #INTO THE PICKLE
            dataman.updatePickle(data)
            textData = makeText( data , ROW_ORDER, ROW_NAMES , OFF_STRING , STATE_TO_UNIT_DICT, nHeadstages )
            csvData = makeText( data , ROW_ORDER, ROW_NAMES, OFF_STRING, STATE_TO_UNIT_DICT, nHeadstages, ',' )
            dataman.updateCSV( csvData )
    print(textData) 


if __name__ == '__main__':
    main()

