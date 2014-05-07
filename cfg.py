"""
    This file holds all the code for parsing values from config.ini.
    This should probably be renamed config.py despite naming conflicts
"""

import configparser

#definitions of the strings as they will appear in config.ini
PATHS = 'PATHS'
PICKLEPATH = 'PICKLEPATH'
CSVPATH = 'CSVPATH'
MCC_DLLPATH = 'MCC_DLL_PATH'

FORMATTING = 'FORMATTING'
ROW_ORDER = 'ROW ORDER'
OFF_STRING = 'OFF STRING'

ROW_NAMES = 'ROW NAMES'
#TODO define the StateNames from mccControl?
HS_TO_UID_DICT = 'HEADSTAGE TO UNIQUE ID'
PROTOCOL_MODE_DICT = 'PROTOCOL MULTICLAMP MODES'
MODE_TO_UNIT_DICT = 'MODE TO UNITS'
STATE_TO_UNIT_DICT = 'STATE TO UNITS'


def makeConfig(configdict,PATH):
    cfg=configparser.ConfigParser()
    cfg.read_dict(configdict)
    with open( PATH , 'w' ) as f:
        cfg.write(f)

def parseConfig(PATH):
    cfg=configparser.ConfigParser()
    cfg.read(PATH)
    for section in example_config: #validate all the sections
        pass
    outputDict={}

    ROW_ORDER = cfg[FORMATTING][ROW_ORDER]
    PICKLEPATH = cfg[PATHS][PICKLEKPATH]
    CSVPATH = cfg[PATHS][CSVPATH]

    MCC_DLLPATH = cfg[PATHS][MCC_DLLPATH]
    HS_TO_UID_DICT = { k:v for k,v in cfg[HS_TO_UID_DICT].items() }
    PROTOCOL_MODE_DICT = { int(k):v.split(' , ') for k,v in cfg[PROTOCOL_MODE_DICT].items() }

    for section,valDict in cfg.items():
        if section == HS_TO_UID_DICT:
            pass
        elif section == PROTOCOL_MODE_DICT:
            pass

        outputDict[section] = None


    return outputDict


#used for default behavior
default_config = {
'DEFAULT':  {
            PICKLEPATH    : "patch_experiment_data.pickle", 
            CSVPATH       : "patch_experiment_data.csv", 
            MCC_DLLPATH   : "C:/Program Files (x86)/Molecular Devices/MultiClamp 700B Commander/3rd Party Support/AxMultiClampMsg", 
            }
}
example_config = {
PATHS : {
        PICKLEPATH    : "patch_experiment_data.pickle", 
        CSVPATH       : "patch_experiment_data.csv", 
        MCC_DLLPATH   : "C:/Program Files (x86)/Molecular Devices/MultiClamp 700B Commander/3rd Party Support/AxMultiClampMsg", 
        }, 

HS_TO_UID_DICT :    {
                    1:'00830476_1',
                    2:'00830476_2',
                    3:'00830691_1',
                    4:'00830691_2',
                    }, 

PROTOCOL_MODE_DICT :    { #conforms to MCC_MODE_DICT naming
                         1:'IC , VC , VC , VC',
                         2:'VC , IC , VC , VC',
                         3:'VC , VC , IC , VC',
                         4:'VC , VC , VC , IC',
                         5:'IC , VC , VC , VC',
                         6:'VC , IC , VC , VC',
                         7:'VC , VC , IC , VC',
                         8:'VC , VC , VC , IC',
                         9:'IC , VC , VC , VC',
                        10:'IC , VC , VC , VC',
                        11:'IC , VC , VC , VC',
                        12:'IC , VC , VC , VC',
                        13:'IC , VC , VC , VC',
                        14:'IC , VC , VC , VC',
                        }, 

FORMATTING :    {
                OFF_STRING  : 'OFF', 
                #these should match the names of keys of the state dict
                ROW_ORDER   : 'Cell,\nMode,\nHolding,\nBridgeBalResist', 
                }, 

ROW_NAMES :   { #all the rows in the state dict, probs should validate
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

                'Serial':'Serial',
                'Channel':'Channel',
                }, 

MODE_TO_UNIT_DICT :   {
                    'IC':'p',
                    'VC':'m'
                    },

STATE_TO_UNIT_DICT :  {
                    'DateTime':'None',
                    'Cell':'None',
                    'Mode':'None ',

                    'HoldingEnable':'None',
                    'Holding':'None #LOOKUP',
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
                    'BridgeBalResist':'M ',

                    'Serial':'None',
                    'Channel':'None',
                    },
}
def main():
    makeConfig(example_dict,'test.ini')

if __name__ == '__main__':
    main()
