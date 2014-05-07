"""
    This file holds all the code for parsing values from config.ini.
    This should probably be renamed config.py despite naming conflicts
"""

import configparser

#definitions of the strings as they will appear in config.ini
_PATHS = 'PATHS'
_PICKLEPATH = 'PICKLEPATH'
_CSVPATH = 'CSVPATH'
_MCC_DLLPATH = 'MCC_DLLPATH'

_FORMATTING = 'FORMATTING'
_OFF_STRING = 'OFF STRING'
_ROW_ORDER = 'ROW ORDER'

_ROW_NAMES = 'ROW NAMES'
#TODO define the StateNames from mccControl?
_HS_TO_UID_DICT = 'HEADSTAGE TO UNIQUE ID'
_PROTOCOL_MODE_DICT = 'PROTOCOL MULTICLAMP MODES'
_MODE_TO_UNIT_DICT = 'MODE TO UNITS'
_STATE_TO_UNIT_DICT = 'STATE TO UNITS'

def getGetHeadstageCount(PATH):
    cfg=configparser.ConfigParser()
    cfg.optionxform=str
    cfg.read(PATH)
    return len(cfg[_HS_TO_UID_DICT])

def parseConfig(PATH):
    cfg=configparser.ConfigParser()
    cfg.optionxform=str #preserve case senstivity
    cfg.read(PATH)

    PICKLEPATH = cfg[_PATHS][_PICKLEPATH]
    CSVPATH = cfg[_PATHS][_CSVPATH]
    MCC_DLLPATH = cfg[_PATHS][_MCC_DLLPATH]

    OFF_STRING = cfg[_FORMATTING][_OFF_STRING]
    ROW_ORDER = cfg[_FORMATTING][_ROW_ORDER].split('\n')

    ROW_NAMES = { k:v for k,v in cfg[_ROW_NAMES].items() }
    HS_TO_UID_DICT = { int(k):v for k,v in cfg[_HS_TO_UID_DICT].items() }
    PROTOCOL_MODE_DICT = { int(k):v.split(' , ') for k,v in cfg[_PROTOCOL_MODE_DICT].items() }
    MODE_TO_UNIT_DICT = { k:v for k,v in cfg[_MODE_TO_UNIT_DICT].items() }
    STATE_TO_UNIT_DICT = { k:v for k,v in cfg[_STATE_TO_UNIT_DICT].items() }


    return PICKLEPATH, CSVPATH, MCC_DLLPATH, OFF_STRING, ROW_ORDER, ROW_NAMES, HS_TO_UID_DICT, PROTOCOL_MODE_DICT, MODE_TO_UNIT_DICT, STATE_TO_UNIT_DICT


def makeConfig(configdict,PATH):
    cfg=configparser.ConfigParser()
    cfg.read_dict(configdict)
    with open( PATH , 'w' ) as f:
        cfg.write(f)



#used for default behavior #FIXME I dont think this works this ways... I think it will add these values to EACH section... which is NOT what we want...
default_config = {
'DEFAULT':  {
            _PICKLEPATH    : "patch_experiment_data.pickle", 
            _CSVPATH       : "patch_experiment_data.csv", 
            _MCC_DLLPATH   : "C:/Program Files (x86)/Molecular Devices/MultiClamp 700B Commander/3rd Party Support/AxMultiClampMsg", 
            }
}
example_config = {
_PATHS : {
        _PICKLEPATH    : "patch_experiment_data.pickle", 
        _CSVPATH       : "patch_experiment_data.csv", 
        _MCC_DLLPATH   : "C:/Program Files (x86)/Molecular Devices/MultiClamp 700B Commander/3rd Party Support/AxMultiClampMsg", 
        }, 

_HS_TO_UID_DICT :    {
                    1:'00830476_1',
                    2:'00830476_2',
                    3:'00830691_1',
                    4:'00830691_2',
                    }, 

_PROTOCOL_MODE_DICT :    { #conforms to MCC_MODE_DICT naming
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

_FORMATTING :    {
                _OFF_STRING  : 'OFF', 
                #these should match the names of keys of the state dict
                _ROW_ORDER   : 'Cell,\nMode,\nHolding,\nBridgeBalResist', 
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

                'Serial':'Serial',
                'Channel':'Channel',
                }, 

_MODE_TO_UNIT_DICT :   {
                    'IC':'p',
                    'VC':'m'
                    },

_STATE_TO_UNIT_DICT :  {
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
