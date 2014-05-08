"""
    This script uses cx_freeze + distuitls to convert inferno into an exe file.
"""

#TODO a batch script to launch a terminal window?

import os

PYTHON_PATH_X86='C:\X86Python33\python.exe'

def makeExe():
    command = 'setup.py bdist_msi'
    os.system(PYTHON_PATH_X86+' '+command)
    pass

def main():
    makeExe()

if __name__ == '__main__':
    main()
