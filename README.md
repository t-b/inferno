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

Usage
-----
Inferno can be run from the command line via inferno.py if you have installed
python and the dependencies listed above. Please see docs/README.md for more
information on using Inferno from source and as a binary.

Building
--------
Inferno must be built against 32bit Python to communicate with AxMuliClampMsg.dll.
Thus to package Inferno into an msi installer using setup.py you will need an x86
python install and cx_Freeze. Once you have these, change PATHON_PATH_X86 in build.py
to match your install location.
