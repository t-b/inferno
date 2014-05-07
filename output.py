""" This is the code for formatting text output to terminal or CSV
"""

from mcc import MCC_MODE_DICT


UNIT_DEFINITIONS = { #used under multiplication with the base unit
'G' : 1E-9,
'M' : 1E-6,
'K' : 1E-3,
'm' : 1E3,
'u' : 1E6,
'n' : 1E9,
'p' : 1E12,
}

def formatUnit(StateVariable, StateDict): #TODO perhaps make it a tuple of unit and format?
    #FIXME this is SUPER slow if we have many rows, should just make and return a dict of multiples!
    #only issue is how to deal with the modes as they come up...
    value = StateDict[StateVariable]
    if StateVariable == 'Holding':
        multiple = UNIT_DEFINITIONS[ MODE_TO_UNIT_DICT[ MCC_MODE_DICT[ StateDict['Mode'] ] ] ] #lol oh god
    else:
        multiple = STATE_TO_UNIT_DICT[StateVariable]
    if multiple == 'None':
        return value
    else:
        return value * multiple

def rowPrintLogic(row,StateDict,delim,OFF_STRING,UNITS):
    #get units
    mode = StateDict['Mode']

    if row == 'Holding':
        if StateDict['HoldingEnable']:
            out = formatUnit(row,StateDict)
            if delim=='\t':
                out='%2.2f'%out
        else:
            out = OFF_STRING
    elif row == 'BridgeBalResist':
        if StateDict['BridgeBalEnable'] and StateDict['Mode'] == 1:
            out = formatUnit(row,StateDict)
            if delim=='\t':
                out='%1.1e'%out
        else:
            out = OFF_STRING
    elif row == 'Mode':
        out = MCC_MODE_DICT[ StateDict[row] ]
    else:
        out = formatUnit(row,StateDict)

    return out

def makeText(data,ROW_ORDER,ROW_NAMES,OFF_STRING,delimiter='\t'):
    # for reference: data = { filename : ( protocolNumber , hsStateDict  ) }
    lines=[]

    numberHeadstages=len(list(data.values())[0][1])
    lineOneList=['HS%s'%n * (n>0) for n in range(numberHeadstages+1)]
    lines.append( '\n'+delimiter.join( lineOneList ) ) #\n is to make it place nice with .split('\n',1)[1]

    for filename , ( protocolNumber , hsStateDict ) in data.items():

        trialNumber=filename[-8:-4]
        lines.append( delimiter.join( ('%s'%trialNumber , '%s'%protocolNumber ,'','','') ) )

        for row in ROW_ORDER:
            values=[ ROW_NAMES[row] ]
            for i in range(1,5):
                values.append( '%s'%rowPrintLogic( row,hsStateDict[i],delimiter,OFF_STRING ) )

            lines.append( delimiter.join(values) )
    return '\n'.join(lines)

    #output format

    #filename format YYYY_MM_DD_nnnn
    #protocol p1 p2 p3 p4 corrisponding to the buttons

    #nnnn   p1
    #       1   2   3   4
    #cell   a   b   c   d 
    #mode   vc  ic  vc  ic #map between mcc + channel and the digitizer input channel
    #holding    -70 OFF OFF -70 #OFF for holding disabled
    #bridge balance


