Todo
----
-2) IF CELLS ARE NOT ON THE HEADSTAGE STILL LOAD ALL THE PROTOCOL STUFF OR PCLAMP WILL ERROR
-1) get rid of newline at the start of the csv file
0) specifying protocol numbers that are blank results in a key error
1) figure out how to set the default path for the conifg, this cannot be set using docopt, it should probably be %INSTALL_DIR%/config.ini or something
2) copying config.ini within the program folder causes administrative bickering, we need a better option :(, I dont want to go full inferno.ini in the users home folder >_< derpmax, something something configurationmanager? yep, that config.ini in program files is not writeable >_< DERP
3) apparently there is a way to call an init script... should look in to that for inferno.bat?
4) set the build option that changes path names...
5) we will need to tailor the defaults for the exe version, if people want to run the script by itself... ok they can edit stuff themselves
6) make it posssible to parse only a subset of the config


Done
----
x) split out the functions in inferno.py to their own file so that they can be tested independently
x) Naming consistency: the program itself is Clampex fix this, pClamp is the suite of software
