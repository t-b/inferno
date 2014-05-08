Inferno
=======
A command line tool for controlling MultiClampCommander and Clampex and saving data.

Dependencies
------------
* x86 python 3.3.x (64bit WILL NOT WORK with the multiclamp dll!)
* docopt
* pywin32

* pClamp10 (Clampex)
* MultiClampCommander (so far only tested with MultiClamp 700B)


Configuration
-------------
Copy config.py.example to config.py and edit it to match your setup.
Most of the dictionaries should be self explanatory.

HS_TO_UID_DICT associates the numbering you use for your headstages 1-n to the
serial number (8 digit number for 700B)  of the Multiclamp follow by an underscore
followed by the channel number (1 or 2). For example 1:'12345678_1' associates your
headstage number 1 to the headstage plugged in to the first channel of the amplifier
that has the serial number 1234567. You should have one entry for each headstage
on your rig.  

PROTOCOL_MODE_DICT associates a list of numbers 1-n to ( representing the UI
buttons moving from left to right in pClamp) to tuples that specify the modes
(voltage clamp "VC", current clamp "IC", or current equals zero "IEZ") that the
protocol assigned to that button uses. The tuple should be the same length as
the number of headstages on your rig.

Button Offsets. In gui.py it is possible to modify the button offsets.
Inferno is currently configured using the default pClamp UI arrangment, but
if you have modified your settings then those button offsets will be wrong.
All offsets are from the top left corner of the window in units of pixels.

Usage
-----
The Clampex window MUST be visible in order to click the protocol buttons
(Dear Molecular Devices, great hardware. Your software sucks.).

MultiClampCommander windows need to be opened but do not need to be visible.

Building
--------
* Inferno must be built against 32bit Python to communicate with AxMuliClampMsg.dll. Thus to package Inferno into an msi installer using setup.py you will need an x86 python install and cx_Freeze. Once you have these, change PATHON_PATH_X86 in build.py to match your install location.

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
