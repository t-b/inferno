"""
    This file holds all the code for parsing values from config.ini.
    This should probably be renamed config.py despite naming conflicts
"""

import os
import configparser
from core.mcc import MCC_MODE_DICT

#definitions of the strings as they will appear in config.ini
_PATHS = 'PATHS'
_PICKLEPATH = 'PICKLEPATH'
_CSVPATH = 'CSVPATH'
_MCC_DLLPATH = 'MCC_DLLPATH'

_OPTIONS = 'OPTIONS'
_PAUSE_ON_LOAD = 'PAUSE ON LOAD'

_FORMATTING = 'FORMATTING'
_NO_CELL_STRING = 'NO CELL STRING'
_OFF_STRING = 'OFF STRING'
_ROW_ORDER = 'ROW ORDER'

_ROW_NAMES = 'ROW NAMES'
#TODO define the StateNames from mccControl?
_HS_TO_UID_DICT = 'HEADSTAGE TO UNIQUE ID'
_PROTOCOL_MODE_DICT = 'PROTOCOL MULTICLAMP MODES'
_STATE_TO_UNIT_DICT = 'STATE TO UNITS'

DEFAULT_USER_DIR = '~/inferno/'

def firstRun(CONFIGPATH):
    if CONFIGPATH == DEFAULT_USER_DIR+'config.ini':
        user_dir = os.path.expanduser(DEFAULT_USER_DIR)
        configpath = os.path.expanduser(CONFIGPATH)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
            makeConfig(example_config,configpath+'.example')
            print('This seems to be the first time you have run Inferno.\n'
                  'An example config has been generated at {0}config.ini.example.\n'
                  'There is also a nicely formated example in the install folder.\n'
                  'Please copy one of these scripts to {0}config.ini and edit it\n'
                  'to match the settings of your rig and protocols.'.format(DEFAULT_USER_DIR)
                 )
            return True
        else:
            return False

def parseConfig(PATH):
    path=os.path.expanduser(PATH)
    if not os.path.exists(path):
        if PATH == DEFAULT_USER_DIR+'config.ini':
            extra = 'Did you copy config.ini.example to config.ini and edit it to match your rig?'
        else: 
            extra = ''
        raise IOError('That config file does not exist!\n%s'%extra)
    cfg=configparser.ConfigParser()
    cfg.optionxform=str #preserve case senstivity
    cfg.read(path)

    PICKLEPATH = os.path.expanduser(cfg[_PATHS][_PICKLEPATH])
    CSVPATH = os.path.expanduser(cfg[_PATHS][_CSVPATH])
    MCC_DLLPATH = cfg[_PATHS][_MCC_DLLPATH]

    try:
        string = cfg[_OPTIONS][_PAUSE_ON_LOAD]
        if string == 'True' or string == '1' or string == 'true':
            PAUSE_ON_LOAD = True
        else: #anything else will be treated as false
            PAUSE_ON_LOAD = False
    except KeyError:
        PAUSE_ON_LOAD = False

    NO_CELL_STRING = cfg[_FORMATTING][_NO_CELL_STRING]
    OFF_STRING = cfg[_FORMATTING][_OFF_STRING]
    ROW_ORDER = cfg[_FORMATTING][_ROW_ORDER].split('\n')

    ROW_NAMES = { k:v for k,v in cfg[_ROW_NAMES].items() }
    HS_TO_UID_DICT = { int(k):v for k,v in cfg[_HS_TO_UID_DICT].items() }
    
    PROTOCOL_MODE_DICT = {}
    for key,string in cfg[_PROTOCOL_MODE_DICT].items():
        if string is not '':
            PROTOCOL_MODE_DICT[ int(key) ] = [s.strip().rstrip() for s in string.split(',')]

    STATE_TO_UNIT_DICT = {}
    for key,string in cfg[_STATE_TO_UNIT_DICT].items():
        fixed_delims = string.replace(' , ',' ').replace(', ',' ').replace(',',' ').replace('\t',' ')
        tup = tuple(fixed_delims.split(' ') )
        STATE_TO_UNIT_DICT[ key ] = tup

    #check MCC_DLLPATH, the others we check later becase we may be creating them
    if not os.path.exists(MCC_DLLPATH):
        raise FileNotFoundError('MCC dll not found at %s. Check your config.'%MCC_DLLPATH)

    #set default formatting for strings
    updateDict = {}
    for mode,tup in STATE_TO_UNIT_DICT.items():
        if len(tup) == 1:
            updateDict[ mode ] = tup[0],'s' #FIXME make sure we aren't missing a comma!
    STATE_TO_UNIT_DICT.update(updateDict)

    #validate protocol mode specifications #TODO make it work same was a NO_CELL_STRING
    nHeadstages = len(HS_TO_UID_DICT)
    validModes = list(MCC_MODE_DICT.values())
    validModes.append('')
    for prot,tup in PROTOCOL_MODE_DICT.items():
        for string in tup:
            if string not in validModes:
                print( 'Warning! In protocol %s a bad mode name "%s" has been detected. Check your config.'%(prot,string) )
        if len(tup) > nHeadstages:
            print('Warning! In protocol %s you listed more modes than your rig'
                  ' has headstages. Inferno will use only as many as needed. Ignoring.'%prot)
        elif len(tup) < nHeadstages:
            raise ValueError('You have %s headstages but you only set modes for'
                             ' %s of them! Check protocol %s in your config! It is OK to leave'
                             ' modes blank but you need commas.'%(nHeadstages,len(tup),prot))




    return PICKLEPATH, CSVPATH, MCC_DLLPATH, PAUSE_ON_LOAD, NO_CELL_STRING, OFF_STRING, ROW_ORDER, ROW_NAMES, HS_TO_UID_DICT, PROTOCOL_MODE_DICT, STATE_TO_UNIT_DICT

def makeConfig(configdict,PATH):
    path = os.path.expanduser(PATH)
    if os.path.exists(path):
        raise IOError('File already exists! If you meant to overwrite it please delete it first.')
    cfg=configparser.ConfigParser()
    cfg.optionxform=str
    cfg.read_dict(configdict)
    with open( path , 'w' ) as f:
        cfg.write(f)


#used for default behavior #FIXME I dont think this works this ways... I think it will add these values to EACH section... which is NOT what we want...


example_config = {
_PATHS : {
        _PICKLEPATH    : DEFAULT_USER_DIR+'patch_experiment_data.pickle', 
        _CSVPATH       : DEFAULT_USER_DIR+'patch_experiment_data.csv', 
        _MCC_DLLPATH   : 'C:/Program Files (x86)/Molecular Devices/MultiClamp 700B Commander/3rd Party Support/AxMultiClampMsg', 
        }, 

_OPTIONS : {
    _PAUSE_ON_LOAD:'False'
},

_HS_TO_UID_DICT :    {
                    1:'12345678_1',
                    2:'12345678_2',
                    3:'87654321_1',
                    4:'87654321_2',
                    }, 

_PROTOCOL_MODE_DICT :    { #conforms to MCC_MODE_DICT naming
                         1:'IC , VC , VC , IEZ',
                         2:'VC , IC , IEZ , VC',
                         3:'VC , IEZ , IC , VC',
                         4:'IEZ , VC , VC , IC',
                         5:'',
                         6:'',
                         7:'',
                         8:'',
                         9:'',
                        10:'',
                        11:'',
                        12:'',
                        13:'',
                        14:'',
                        15:'',
                        16:'',
                        17:'',
                        }, 

_FORMATTING :    {
                _NO_CELL_STRING : 'xx',
                _OFF_STRING     : 'OFF', 
                #these should match the names of keys of the state dict
                _ROW_ORDER      : 'Cell\nMode\nHolding\nMeter\nBridgeBalResist', 
                }, 

_ROW_NAMES :   { #all the rows in the state dict, probs should validate
                'DateTime':'Time',
                'Cell':'Cell',
                'Mode':'Mode', 

                'HoldingEnable':'HoldON',
                'Holding':'Hold',
                'PrimarySignal':'PS',
                'PrimarySignalGain':'PSGain',
                'PrimarySignalLPF':'PSLFP',
                'PipetteOffset':'POffset',

                'FastCompCap':'FCCap',
                'SlowCompCap':'SCCap',
                'FastCompTau':'FCTau',
                'SlowCompTau':'SCTau',
                'SlowCTX20Enable':'Tau20x',

                'BridgeBalEnable':'BBalON',
                'BridgeBalResist':'BBal',

                'Meter':'Meter',
                'MeterVoltage':'MVolts',
                'MeterResist':'MResist',
                'MeterCurrent':'MCurr',
                'MeterIrms':'MIrms',
                'MeterResistEnable':'MRE',
                'MeterVR':'MVR',
                'MeterIrmsEnable':'MIE',
                'MeterII':'MII',

                'Serial':'Serial',
                'Channel':'Channel',
                }, 

_STATE_TO_UNIT_DICT :  {
                    'IC':'p, 3.1f',
                    'VC':'m, 3.1f',

                    'MeterVoltage':'m, 3.1f',
                    'MeterResist':'M, 3.1f',
                    'MeterCurrent':'p, 3.1f',
                    'MeterIrms':'p, 3.1f',
                    'MeterResistEnable':'None',
                    'MeterVR':'None',
                    'MeterIrmsEnable':'None',
                    'MeterII':'None',

                    'DateTime':'None',
                    'Cell':'None',
                    'Mode':'None ',

                    'HoldingEnable':'None',
                    'Holding':'None',
                    'PrimarySignal':'None',
                    'PrimarySignalGain':'None',
                    'PrimarySignalLPF':'None',
                    'PipetteOffset':'m ',

                    'FastCompCap':'p ',
                    'SlowCompCap':'p ',
                    'FastCompTau':'u ',
                    'SlowCompTau':'u ',
                    'SlowCTX20Enable':'None',

                    'BridgeBalEnable':'None',
                    'BridgeBalResist':'M, 3.1F',

                    'Serial':'None',
                    'Channel':'None',
                    },
}
def main():
    badstring='IC,VC,asdf,'
    badstring=',,,'
    badstring='IC,VC,asdf,asdf'
    makeConfig(example_config,'test.ini')
    badConfig = example_config #pretty sure this is by reference
    badConfig[_PROTOCOL_MODE_DICT][1]=badstring
    makeConfig(badConfig,'bad.ini')
    parseConfig('bad.ini')

if __name__ == '__main__':
    main()
