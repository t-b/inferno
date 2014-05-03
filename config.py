PICKLEPATH  = "patch_experiment_data.pickle"
CSVPATH     = "patch_experiment_data.csv"
MCC_DLLPATH = "C:/Program Files (x86)/Molecular Devices/MultiClamp 700B Commander/3rd Party Support/AxMultiClampMsg"

HS_TO_UID_DICT = { #XXX CHECK MEEEEE!!
1:'00830691_1',
2:'00830691_2',

3:'00830476_1',
4:'00830476_2',
}

PROTOCOL_MODE_DICT = { #can also use 'ize'
1:('i','v','v','v'),
2:('v','i','v','v'),
3:('v','v','i','v'),
4:('v','v','v','i'),
5:('i','v','v','v'),
6:('i','v','v','v'),
7:('i','v','v','v'),
8:('i','v','v','v'),
9:('i','v','v','v'),
10:('i','v','v','v'),
11:('i','v','v','v'),
12:('i','v','v','v'),
13:('i','v','v','v'),
14:('i','v','v','v'),
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

