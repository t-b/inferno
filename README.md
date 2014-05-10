Inferno
=======
A command line tool for controlling MultiClampCommander and Clampex and saving data.

Installation
------------
To install a standalone version of Inferno please download and install the
most recent MSI from the [releases page](https://github.com/tgbugs/inferno/releases).
Please check the installation folder and read the README.txt provided there
(it is the same as [docs/README.md](docs/README.md) so you can read that
instead). Otherwise you can simply download the zip file or use git clone and
run Inferno from inferno.py.

Usage
-----
If you do not use the standalone installer, Inferno can be run from the command
line via inferno.py if you have installed python and the dependencies listed
below. The [README.md in docs](docs/README.md) also has information relevant
for using Inferno from source.

Dependencies
------------
* x86 python 3.3.x (64bit WILL NOT WORK with the multiclamp dll!)
* docopt
* pywin32
* cx_Freeze (if you are building)

Supported Programs
------------------
* pClamp10 (Clampex)
* MultiClampCommander (so far only tested with MultiClamp 700B)

Building
--------
Inferno must be built against 32bit Python to communicate with AxMuliClampMsg.dll.
Thus to package Inferno into an msi installer using setup.py you will need an x86
python install and cx_Freeze. Once you have these, change `PATHON_PATH_X86` in build.py
to match your install location.

Extending Inferno
-----------------
Inferno currently only supports Clampex and MultiClampCommander. However there
are only three functions that need to be implemented to control a data acquisition
program: `LoadProtocol`, `Record`, and `GetFilename` (and possibly `IsOn`?).
