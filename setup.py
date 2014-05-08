import sys #why do we need this again?
from cx_Freeze import setup, Executable

executables = [
    Executable('inferno.py',
               icon = None,
               appendScriptToExe=True,
               appendScriptToLibrary = False,
               excludes = ['IPython'],
              )
]

include_files = [
    'config.ini.example',
    'docs/README.txt',
    'inferno.bat',
]

buildOptions = { 'create_shared_zip' : False,
                 'include_files' : include_files,
               }


setup(name = 'inferno',
      version = '0.0.1',
      description = 'Inferno: electrophysiology in a shell.',
      options = { 'build_exe' : buildOptions } ,
      executables = executables,
     )


