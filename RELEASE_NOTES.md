v0.0.5
------
Clampex verion 9 now supported.

Added the ability to pause Inferno after loading a protocol in case the user
needs to tweak the protocol for that particular cell.

This option can be set globally via config.ini or on the command line with `-s` or `--stop`.

Unless `PAUSE ON LOAD = True` is added to the `[OPTIONS]` section of the config
or `-s` is set on the command line Inferno will click record immediately after
loading the protocol.

While this feature can be quite useful there is a nasty side effect from using
the GUI to click the buttons: the terminal window loses focus.
Therefore you can __click the terminal window to advance__. Hopefully clicking the
mouse will not cause problems later when it needs to move to click the record button.

The `[OPTIONS]` section is optional, default values are shown in the example config.

#### New config sections
```
[OPTIONS]
PAUSE ON Load = False
```

#### New command line options
`-s --stop`


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
