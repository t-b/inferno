v0.0.5
------
Added the ability to pause Inferno after loading a protocol incase the user
needs to tweak the protocol for that particular cell. This option can be set
globally via config.ini or on the command line with `-s` or `--stop`. Unless
`PAUSE ON LOAD = True` is added to the options section of the config or -s is
set on the command line Iferno will click record immediately after loading the
protocol.

The OPTIONS section is optional, default values are show in the example config.

#### New config sections
[OPTIONS]
PAUSE ON Load = False

#### New command line options
-s --stop


v0.0.4
------
Added the ability to print the meter values for MultiClampCommander.
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
