import re
from datetime import datetime
import inspect as ins
from sys import stdout,stdin
from time import sleep

class mccFuncs: #FIXME add a way to get the current V and I via... telegraph?
    def __init__(self, mcc=None):
        try:
            if mcc.__class__.__name__ is not 'mccControl':
                raise TypeError('wrong controller type')
        except:
            raise
        self.mcc=mcc

        self.MCCstateDict={} #this is ALL the states collected ever

    def setGain(self,value=1):
        self.mcc.SetPrimarySignalGain(value)
        print('Primary signal gain set to %s'%value)
        return self

    def allGain(self,value=1):
        self.mcc.selectMC(0)
        self.mcc.SetPrimarySignalGain(value)
        self.mcc.selectMC(1)
        self.mcc.SetPrimarySignalGain(value)
        return self

    def setMCCState(self,stateList):
        """ ste the mcc state from a mcc state dict list """
        for state in stateList:
            self.mcc.selectMC(state['Channel'])
            self.mcc.SetMode(state['mode'])
            self.mcc.SetHolding(state['Holding'])
            self.mcc.SetHoldingEnable(state['HoldingEnable'])
            self.mcc.SetPrimarySignal(state['PrimarySignal'])
            self.mcc.SetPrimarySignalGain(state['PrimarySignalGain'])
            self.mcc.SetPrimarySignalLPF(state['PrimarySignalLPF'])
        return self

    def getMCCState(self,uniqueIDs=None): #FIXME this function and others like it should probably be called directly by dataman?
        if not uniqueIDs:
            uniqueIDs = self.mcc.mcDict
        #print('hMCCmsg outer',self.mcc.hMCCmsg)
        def base(state):
            state['Serial']=self.mcc.getSerial()
            state['Channel']=self.mcc.getChannel()
            state['HoldingEnable']=self.mcc.GetHoldingEnable()
            state['Holding']=self.mcc.GetHolding()
            state['PrimarySignal']=self.mcc.GetPrimarySignal()
            state['PrimarySignalGain']=self.mcc.GetPrimarySignalGain() #also in abf file and already handled by AxonIO
            state['PrimarySignalLPF']=self.mcc.GetPrimarySignalLPF() #also in abf file
            state['PipetteOffset']=self.mcc.GetPipetteOffset()

            #XXX ONLY RELEVANT FOR MODE 0 (VC)
            state['FastCompCap']=self.mcc.GetFastCompCap()
            state['SlowCompCap']=self.mcc.GetSlowCompCap()
            state['FastCompTau']=self.mcc.GetFastCompTau()
            state['SlowCompTau']=self.mcc.GetSlowCompTau()
            state['SlowCTX20Enable']=self.mcc.GetSlowCompTauX20Enable()

            #XXX ONLY RELEVANT FOR MODE 1 (IC)
            state['BridgeBalEnable']=self.mcc.GetBridgeBalEnable()
            state['BridgeBalResist']=self.mcc.GetBridgeBalResist()
            state['DateTime']=datetime.now()

        #modeDict={0:vc,1:ic,2:iez}
        stateDict={}
        for uniqueID in uniqueIDs:
            channelDict={} #XXX does this work? that would be cool?
            self.mcc.selectUniqueID(uniqueID)
            mode=self.mcc.GetMode() #in the event we want to do something fancy?
            channelDict['Mode']=mode
            base(channelDict)
            stateDict[uniqueID]=channelDict
        self.MCCstateDict[datetime.utcnow()]=stateDict
        return stateDict

    def printMCCstate(self):
        print(re.sub('\), ',')\r\n',str(self.MCCstateDict)))
        return self


    def set_hs0(self):
        print('Setting headstage 0')
        self.mcc.selectMC(0)
        self.current_headstage=0
        return self
    def set_hs1(self):
        print('Setting headstage 1')
        self.mcc.selectMC(1)
        self.current_headstage=1 #TODO use this to link cells to the headstage!
        return self
    def set_hsAll(self): #FIXME
        self.ALL_HS=True

    def autoOffset(self):
        self.mcc.AutoPipetteOffset()
    def autoCap(self):
        self.mcc.AutoFastComp()
        self.mcc.AutoSlowComp()
    def setVCholdOFF(self):
        self.mcc.SetMode(0)
        self.mcc.SetHoldingEnable(0)
    def setVCholdON(self):
        self.mcc.SetMode(0)
        self.mcc.SetHoldingEnable(1)

    def setVChold(self,holding_volts):
        #print(holding_volts)
        self.mcc.SetMode(0)
        print(holding_volts)
        self.mcc.SetHolding(float(holding_volts))
        h=self.mcc.GetHolding()
        print(h)
        #sleep(.001) #FIXME trying to figure out why holding set to -1000mV
        #self.mcc.SetHoldingEnable(1)
    def setICnoHold(self):
        self.mcc.SetMode(1)
        self.mcc.SetHoldingEnable(0)

    def allVChold(self,holding_volts):
        self.mcc.selectMC(0)
        self.mcc.SetMode(0)
        self.mcc.SetHolding(float(holding_volts))
        #self.mcc.SetHoldingEnable(1)
        self.mcc.selectMC(1)
        self.mcc.SetMode(0)
        self.mcc.SetHolding(float(holding_volts))
        #self.mcc.SetHoldingEnable(1)
        return self

    def allIeZ(self):
        self.mcc.selectMC(0)
        self.mcc.SetMode(2)
        self.mcc.selectMC(1)
        self.mcc.SetMode(2)
        return self
    def allVCnoHold(self):
        #try:
        self.mcc.selectMC(0)
        self.mcc.SetMode(0)
        self.mcc.SetHoldingEnable(0)
        self.mcc.selectMC(1)
        self.mcc.SetMode(0)
        self.mcc.SetHoldingEnable(0)
        #except:
            #raise BaseException
        return self
    def allVChold_60(self):
        self.mcc.selectMC(0)
        self.mcc.SetMode(0)
        self.mcc.SetHolding(-.06)
        self.mcc.SetHoldingEnable(1)
        self.mcc.selectMC(1)
        self.mcc.SetMode(0)
        self.mcc.SetHolding(-.06)
        self.mcc.SetHoldingEnable(1)
        return self
    def allICnoHold(self):
        self.mcc.selectMC(0)
        self.mcc.SetMode(1)
        self.mcc.SetHoldingEnable(0)
        self.mcc.selectMC(1)
        self.mcc.SetMode(1)
        self.mcc.SetHoldingEnable(0)
        return self
    def testZtO(self,holding_voltage):
        self.mcc.selectMC(0)
        self.mcc.SetMode(1)
        self.mcc.SetHoldingEnable(0)
        self.mcc.selectMC(1)
        self.mcc.SetMode(0)
        self.mcc.SetHolding(float(holding_voltage))
        self.mcc.SetHoldingEnable(1)
        return self
    def testOtZ(self,holding_voltage):
        self.mcc.selectMC(0)
        self.mcc.SetMode(0)
        self.mcc.SetHolding(float(holding_voltage))
        self.mcc.SetHoldingEnable(1)
        self.mcc.selectMC(1)
        self.mcc.SetMode(1)
        self.mcc.SetHoldingEnable(0)
        return self
    def zeroVChold_60(self):
        self.mcc.selectMC(0)
        self.mcc.SetMode(0)
        self.mcc.SetHolding(-.06)
        self.mcc.SetHoldingEnable(1)
        return self
    def oneVChold_60(self):
        self.mcc.selectMC(1)
        self.mcc.SetMode(0)
        #self.mcc.poops(1) #awe, this is broken now due to something
        self.mcc.SetHolding(-.06)
        self.mcc.SetHoldingEnable(1)
        return self
    def cleanup(self):
        try:
            pass
            #self.mcc.cleanup()
            #self.mcc.DestroyObject()
            #print(self.mcc.__class__,'handler destroyed')
        except:
            pass


#@hardware_interface('ESP300')

def main():
    from mcc import mccControl
    from IPython import embed
    from config import MCC_DLLPATH
    mcc=mccFuncs(mccControl(MCC_DLLPATH))
    embed()

__all__=(
    'mccFuncs',
)
if __name__=='__main__':
    main()
