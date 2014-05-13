v0.0.4
------
Added the ability to print the meter values for MultiClampCOmmander.
Please update your config if you want to be able to print these values.

#### New StateVariables saved:
 * MeterVR
 * MeterResistEnable
 * MeterII
 * MeterIrmsEnable

#### New row values that can be printed:
 * Meter
 * MeterVR
 * MeterResistEnable
 * MeterII
 * MeterIrmsEnable

#### New print rows that can have units set
 * MeterVoltage
 * MeterResist
 * MeterCurrent
 * MeterIrms

__NOTE__: I have not tested the new configs against old pickle dictionary strcutre.
It looks like I have a try/except in makeText that handles this already by
simply dropping rows that are not found in the dict.


v0.0.3
------
Initial release.
