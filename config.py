PICKLEPATH  = "patch_experiment_data.pickle"
CSVPATH     = "patch_experiment_data.csv"
MCC_DLLPATH = "C:/Program Files (x86)/Molecular Devices/MultiClamp 700B Commander/3rd Party Support/AxMultiClampMsg"

HS_TO_UID_DICT = { #XXX CHECK MEEEEE!!
1:'00830476_1',
2:'00830476_2',
3:'00830691_1',
4:'00830691_2',
}

PROTOCOL_MODE_DICT = { #conforms to MCC_MODE_DICT naming
 1:('IC','VC','VC','VC'),
 2:('VC','IC','VC','VC'),
 3:('VC','VC','IC','VC'),
 4:('VC','VC','VC','IC'),
 5:('IC','VC','VC','VC'),
 6:('IC','VC','VC','VC'),
 7:('IC','VC','VC','VC'),
 8:('IC','VC','VC','VC'),
 9:('IC','VC','VC','VC'),
10:('IC','VC','VC','VC'),
11:('IC','VC','VC','VC'),
12:('IC','VC','VC','VC'),
13:('IC','VC','VC','VC'),
14:('IC','VC','VC','VC'),
}

ROW_ORDER = [ #these should match the names of keys of the state dict
'Cell',
'Mode',
'Holding',
'BridgeBalResist',
]

ROW_NAMES = { #all the rows in the state dict, probs should validate
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
}

