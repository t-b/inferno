"""
    This script uses cx_freeze + distuitls to convert inferno into an exe file.
"""

#TODO a batch script to launch a terminal window?

import os

PYTHON_PATH_X86='C:\X86Python33\python.exe'

def pre():
    os.system('cp docs\README.md docs\README.txt')

def post():
    os.system('rm docs\README.txt')

def makeExe():
    command = 'setup.py bdist_msi'
    os.system(PYTHON_PATH_X86+' '+command)
    pass

def main():
    pre()
    makeExe()
    post()

if __name__ == '__main__':
    main()
