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
    ('docs/README.md','README.txt'),
    'inferno.bat',
]

buildOptions = { 'create_shared_zip' : False,
                 'include_files' : include_files,
               }

setupOptions = { 'build_exe' : buildOptions,
                 'bdist_msi' : {'add_to_path':True,'upgrade_code':'inferno1'}
               }

setup(name = 'inferno',
      version = '0.0.2',
      description = 'Inferno: electrophysiology in a shell.',
      options = setupOptions,
      executables = executables,
     )


