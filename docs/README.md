Inferno
=======
A command line tool for controlling MultiClampCommander and Clampex and saving data.


Configuration
-------------
Copy config.ini.example to config.ini and edit it to match your setup. Most
sections in config.ini should be self explanatory. All sections are required.

[HEADSTAGE TO UNIQUE ID] associates the numbers you use for your headstages 1-n
to the serial number (8 digit number for 700B)  of the Multiclamp follow by an
underscore followed by the channel number (1 or 2). For example 1 = 12345678_1
associates your headstage number 1 to the headstage plugged in to the first
channel of the amplifier that has the serial number 1234567. You should have one
entry for each headstage on your rig.  

[PROTOCOL MULTICLAMP MODES] associates a list of numbers 1-14, which represent
the UI buttons moving from left to right in Clampex, to tuples that specify the
modes (voltage clamp "VC", current clamp "IC", or current equals zero "IEZ")
that the protocol assigned to that button uses. The tuple should be the same
length as the number of headstages on your rig. __You need to assign your
protocols to the UI buttons for Inferno to work properly.__

[STATE TO UNITS] tell Inferno how to display numbers from MultiClampCommander
using tuples of an SI prefix and python string formatting syntax. Please see
[the python documentation](https://docs.python.org/3.3/library/string.html#format-specification-mini-language)
for reference. If you do not specify a format it will default to %s. Note that
MultiClampCommander stores all numbers as the base unit (V,A, etc). Note also
that IC and VC are in fact specified by checking the Mode setting for holding
however since there is no overlap of keys we keep them in [STATE TO UNITS]

Button Offsets. In gui.py it is possible to modify the button offsets.
Inferno is currently configured using the default Clampex UI arrangment, but
if you have modified your settings then those button offsets will be wrong.
All offsets are from the top left corner of the window in units of pixels.

Usage
-----
The Clampex window MUST be visible in order to click the protocol buttons
(Dear Molecular Devices, great hardware. Your software sucks.).

MultiClampCommander windows need to be opened but do not need to be visible.

Notes
-----
Inferno ONLY sets the the mode of the patch clamp amplifier. It is possible to
programatically set and adjust many other things, however there is a risk of
loosing cells due to misconfigured settings and takes time to develop properly.

Known Issues
------------
It takes time for values set in MultiClampCommander to propagate via telegraph
to Clampex. We sleep(1) to prevent erros when loading Clampex protocol too soon.
We have only tested with 4 headstages, it may take longer if you use more.
