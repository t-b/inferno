v0.0.4
------
Added the ability to print the meter values for MultiClampCOmmander.
Please update your config if you want to be able to print these values.

__NOTE__: I have not tested the new configs against old pickle dictionary strcutre.
It looks like I have a try/except in makeText that handles this already by
simply dropping rows that are not found in the dict.

#### New StateVariables saved:
 * MeterVR
 * MeterResistEnable
 * MeterII
 * MeterIrmsEnable

#### New Row values that can be printed:
 * Meter
 * MeterVoltage
 * MeterResist
 * MeterCurrent
 * MeterIrms
 * MeterVR
 * MeterResistEnable
 * MeterII
 * MeterIrmsEnable


v0.0.3
------
Initial release.
