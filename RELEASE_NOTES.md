v0.0.4
------
Added the ability to print the meter values for MultiClampCOmmander.
Please update your config if you want to be able to print these values.

__NOTE__: I have not tested the new configs against old pickle dictionary strcutre.
I suspect that there will be key errors if you try to use a new config on an old dict.
The easiest way to fix this is to keep a copy of your old config and use a new pickle file.
Alternately submit a bug or a pull request that fixes makeText in output.py

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
