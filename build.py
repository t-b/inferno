"""
    This script uses cx_freeze to convert inferno into an exe file.
    It then wraps it up with README.md and LICENSE and example configs
    And puts it in a single folder, the source (ie all the scripts)
    will be placed in ./src/ inside the folder. All will be zipped and
    a version appended.
"""

#TODO a batch script to launch a terminal window?

import os

PYTHON_PATH_X86='C:\X86Python33\python.exe'

def makeExe():
    command = 'setup.py bdist_msi'
    os.system(PYTHON_PATH_X86+' '+command)
    pass

def copyFiles():
    pass

def copySrc():
    pass

def zipIt():
    pass

def main():
    makeExe()


if __name__ == '__main__':
    main()
