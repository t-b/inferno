"""
    This is the code for formatting text output to terminal or CSV
"""

from mcc import MCC_MODE_DICT

#hrm, the number of functions I have to pass STATE_TO_UNIT_DICT through really suggests there might be some use in having shared state?

PREFIX_DEFINITIONS = { #used under multiplication with the base unit
'G' : 1E-9,
'M' : 1E-6,
'K' : 1E-3,
'None' : 1,
'm' : 1E3,
'u' : 1E6,
'n' : 1E9,
'p' : 1E12,
}

def meterFormatting(StateVariable, StateDict, OFF_STRING, STATE_TO_UNIT_DICT):
    if StateVariable == 'Meter':
        if StateDict['Mode'] == 0:
            if StateDict['MeterResistEnable']:
                return formatUnit('MeterResist',StateDict,STATE_TO_UNIT_DICT)
            else:
                return formatUnit('MeterVoltage',StateDict,STATE_TO_UNIT_DICT)
        else: #mode 1 or 2 are current clamp
            if StateDict['MeterIrmsEnable']:
                return formatUnit('MeterIrms',StateDict,STATE_TO_UNIT_DICT)
            else:
                return formatUnit('MeterCurrent',StateDict,STATE_TO_UNIT_DICT)
    elif StateVariable == 'MeterVoltage':
        if StateDict['MeterResistEnable']:
            return OFF_STRING
    elif StateVariable == 'MeterResist':
        if not StateDict['MeterResistEnable']:
            return OFF_STRING
    elif StateVariable == 'MeterCurrent':
        if StateDict['MeterIrmsEnable']:
            return OFF_STRING
    elif StateVariable == 'MeterIrms':
        if not StateDict['MeterIrmsEnable']:
            return OFF_STRING
    #if the meters were actually in that state, or MeterVR, MeterII raw
    return formatUnit(StateVariable,StateDict,STATE_TO_UNIT_DICT)

def formatUnit(StateVariable, StateDict, STATE_TO_UNIT_DICT):
    #FIXME this is SUPER slow if we have many rows, should just make and return a dict of multiples!
    if StateVariable == 'MeterVoltage' or StateVariable == 'MeterResist':
        value = StateDict['MeterVR']
    elif StateVariable == 'MeterCurrent' or StateVariable == 'MeterIrms':
        value = StateDict['MeterII']
    else:
        #only issue is how to deal with the modes as they come up...
        value = StateDict[StateVariable] #FIXME for some reason when we run this with a single cell... OH it is because the program is expect EXACTLY n headstages, need to fix that stat!

    if StateVariable == 'Holding':
        prefix , fmt = STATE_TO_UNIT_DICT[ MCC_MODE_DICT[ StateDict['Mode'] ] ] #lol oh god
        multiple = PREFIX_DEFINITIONS[ prefix ]
        format_string = '%'+fmt
    else:
        prefix , fmt = STATE_TO_UNIT_DICT[StateVariable] #XXX NOTE the 's' is added in parse
        multiple = PREFIX_DEFINITIONS[ prefix ]
        format_string = '%'+fmt

    if multiple == 1:
        return format_string%value
    else:
        return format_string%( value * multiple )

def rowPrintLogic(row,StateDict,delim,OFF_STRING, STATE_TO_UNIT_DICT):
    #get units
    mode = StateDict['Mode']

    if row == 'Holding':
        if StateDict['HoldingEnable']:
            out = formatUnit(row,StateDict,STATE_TO_UNIT_DICT)
        else:
            out = OFF_STRING
    elif row == 'BridgeBalResist':
        if StateDict['BridgeBalEnable'] and StateDict['Mode'] == 1:
            out = formatUnit(row,StateDict,STATE_TO_UNIT_DICT)
        else:
            out = OFF_STRING
    elif row == 'Mode':
        out = MCC_MODE_DICT[ StateDict[row] ]
    elif row.count('Meter'):
        out = meterFormatting(row,StateDict,OFF_STRING,STATE_TO_UNIT_DICT)
    else:
        out = formatUnit(row,StateDict,STATE_TO_UNIT_DICT)

    return out

def makeText(data,ROW_ORDER,ROW_NAMES,OFF_STRING,STATE_TO_UNIT_DICT,numberHeadstages,delimiter='\t'):
    # for reference: data = { filename : ( protocolNumber , hsStateDict  ) }
    lines=[]

    lineOneList=['HS%s'%n * (n>0) for n in range(numberHeadstages+1)]
    lines.append( '\n'+delimiter.join( lineOneList ) ) #\n is to make it place nice with .split('\n',1)[1]

    for filename , ( protocolNumber , hsStateDict ) in data.items():

        trialNumber=filename[-8:-4]
        lines.append( delimiter.join( ('%s'%trialNumber , '%s'%protocolNumber ,'','','') ) )

        for row in ROW_ORDER:
            values=[ ROW_NAMES[row] ]
            for i in range(1,numberHeadstages+1):
                try: 
                    values.append( '%s'%rowPrintLogic( row,hsStateDict[i],delimiter,OFF_STRING,STATE_TO_UNIT_DICT ) )
                except KeyError:
                    values.append('') #blank cell if we weren't using that row

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


