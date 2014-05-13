Inferno
=======
A command line tool for controlling MultiClampCommander and Clampex and saving data.

Inferno is an open source project licensed under the MIT license.
Source code is available at http://github.com/tgbugs/inferno.

A pretty version of this README is available at:
https://github.com/tgbugs/inferno/tree/dev/docs/README.md

Please submit any bugs or feature requests to the github issue tracker.

Configuration
-------------
By default Inferno looks for a configuration file in ~/inferno/config.ini.
To create [~/inferno/config.ini.example](../config.ini.example)
run `inferno setup`. You should copy config.ini.example located in the install
folder (same place as this README), or the example created by inferno setup to
config.ini and edit it to match your setup (the example in the install folder
has nicer formatting). Most sections in config.ini should be self explanatory.
All sections are required. __Please test your config settings and the general
operation of Inferno on your rig before conducting real experiments__

[HEADSTAGE TO UNIQUE ID] associates the numbers you use for your headstages 1-n
to the serial number (8 digit number for 700B)  of the Multiclamp follow by an
underscore followed by the channel number (1 or 2). For example 1 = 12345678_1
associates your headstage number 1 to the headstage plugged in to the first
channel of the amplifier that has the serial number 1234567. You should have one
entry for each headstage on your rig.  

[PROTOCOL MULTICLAMP MODES] associates a list of numbers 1-17, which represent
the UI buttons moving from left to right in Clampex, to tuples that specify the
modes (voltage clamp VC, current clamp IC, or current equals zero IEZ)
that the protocol assigned to that button uses. The tuple should be the same
length as the number of headstages on your rig. __You need to assign your
protocols to the UI buttons for Inferno to work properly.__ The buttons in
question can be seen here:

![alt text](https://raw.githubusercontent.com/tgbugs/inferno/dev/docs/clxbutts.jpg "Yep, those")

[STATE TO UNITS] tell Inferno how to display numbers from MultiClampCommander
using tuples of an SI prefix and python string formatting syntax. Please see
[the python documentation](https://docs.python.org/3.3/library/string.html#format-specification-mini-language)
for reference. If you do not specify a format it will default to normal string
formatting. Note that MultiClampCommander stores all numbers as the base unit
(V,A, etc). Note also that IC and VC are in fact specified by checking the Mode
setting for a headstage, however since there is no overlap of keys we keep
them in [STATE TO UNITS].

Button Offsets. In gui.py it is possible to modify the button offsets.
Inferno is currently configured using the default Clampex UI arrangment, but
if you have modified your settings then those button offsets will be wrong and
you should return the Clampex GUI to the default settings (as seen above).
All offsets are from the top left corner of the window in units of pixels.

Usage
-----
To run Inferno start up Clampex and your MultiClampCommander windows and open
a command propt and type `inferno` or double click `run_inferno.bat` in the
program folder.

A couple of examples of how to use Inferno for on a rig with four headstages:

`inferno run cell1 cell2 cell3 cell4 -p 1`

loads the program associated with the first Clampex button and associates
cell1 with headstage 1, cell 2 with headstage 2, etc. If you don't have cells
on all four headstages at once you could do the following:

`inferno run a xx b -p 3`

In thise case you have associated the cell with identifier `a` to headstage 1,
left headstage two blank by using `xx` to mark it as blank, 
associated the cell with identifier `b` to headstage three, and left the fourth
headstage blank by not entering anything at all. Cell identifiers are case
sensitive. You can set what string signifies that there is no cell on a headstage
in your config with the `NO_CELL_STRING` value.

##### Details
The Inferno installer adds inferno.exe to the windows PATH environment variable.
You can open a command prompt anywhere and run `inferno --help` to get started.

A batch file `run_inferno.bat` is also available to automatically open a command
prompt and execute `inferno --help`.

If you want to make a shortcut use `run_inferno.bat` since running `inferno.exe`
from windows explorer won't do anything useful.

__The Clampex window MUST be visible so that Inferno can click the protocol buttons__
(Dear Molecular Devices, great hardware. Your software sucks.).

MultiClampCommander windows need to be opened but do not need to be visible.

Text output
-----------
Inferno saves a subset of the data it collects formatted as text that is easy
to read for analysis (all the data is saved in the binary). You can control
what is displayed and how it is formatted using the config as mentioned above.
It is also possible to write (or rewrite) the CSV file with different formatting
by modifying your config and running `inferno makecsv`. By defautl this uses the
pickle file and the csv file listed in your config but you can specify different
files using options on the command line.

__Caution__: The current implementation of 'Meter' row printing is a bit janky.
It will print the value of whichever mode that meter was in when the trial was
run, so if you had the voltage/resist meter in resist mode it will format and
print the resist value. Since units are not explictly listed it can be hard to
tell from the value alone what state the meter was in. If you need to know for
sure you can always print MeterVoltage or MeterCurrent.

Notes
-----
Inferno ONLY sets the mode (IC,VC,IEZ) of the patch clamp amplifier. It is
possible to automatically set many other values via the MCC API, however for
the time being we will leave those controls in the hands of the experimenter.

__WARNING:__ Inferno stores binary data in a python dictionary using filenames as
keys. If you change folders from day to day and reuse filenames without changing
which pickle file you save to (in the config), you will loose data. Inferno will
warn you if it detects that you are overwriting existing entries in a pickle file.

Known Issues
------------
It takes time for values set in MultiClampCommander to propagate via telegraph
to Clampex. We sleep(1) to prevent errors when loading the Clampex protocol too
soon. We have only tested with 4 headstages, it may take longer if you use more.
