import sys
from cx_Freeze import setup, Executable
from inferno import __version__

executables = [
    Executable('inferno.py',
               icon = None,
               appendScriptToExe=True,
               appendScriptToLibrary = False,
               excludes = ['IPython'],
               replacePaths = [('*','*')],
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
bdistOptions = { 'add_to_path':True,
                 'upgrade_code':'{AFA68806-4E2B-406a-858B-880B842ADA05}',
}

setupOptions = { 'build_exe' : buildOptions,
                 'bdist_msi' : bdistOptions,
               }

setup(name = 'inferno',
      version = __version__,
      author = 'Tom Gillespie',
      author_email = 'tgbugs@gmail.com',
      url = 'https://github.com/tgbugs/inferno',
      license = 'MIT',
      description = 'Inferno: electrophysiology in a shell.',
      platforms = ['windows'],
      install_requires = ['docopt','pywin32'],
      options = setupOptions,
      executables = executables,
     )


