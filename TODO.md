Todo
----
0) rather irritating issue in which dataio will create a new pickle file and csv file if one does not exist when using inferno makecsv, nbd for now, but decidedly a bug

6) make it posssible to parse only a subset of the config

8) may need to add a way to write to a different binary file too depending on file structure

9) alternately alert the user and ask if this is what they wanted to do, if no, we need to figure out how to sanely save both pieces of data...

10) update how we use config parser to support multiple config file locations?

11) make checking to see if the program is on explict

12) possibly rework how the data acquistion interacts such that it is easier to add new systems, basically we just need a type that provides access to IsOn, LoadProtocol, Record, and GetFilename

13) make it possible to choose how to format the filename data and the protocol name data

14) use folders to make the source more readable

15) define meter naming schemes in mcc.py explicitly




Done
----
x) sanitize/properly handle type errors from the cli

x) add an optional pause via PAUSE_AFTER_LOAD

x) adjust for clampex 9 filenaming scheme by looking for [], or not? was the bug just with 0000? nope, just with certain scope types?!? just replace('[','') all the things

x) FIXME the structure of the makecsv options is not correct, you should be able to spec a csv file without having to spec a binary file!

x) make it possible to easily extend inferno with new modules for acquisition programs other than Clampex10, eg Clampex9...

x) specifying protocol numbers that are blank results in a key error

x) we will need to tailor the defaults for the exe version, if people want to run the script by itself... ok they can edit stuff themselves

x) figure out how to set the default path for the conifg, this cannot be set using docopt, it should probably be %INSTALL_DIR%/config.ini or something

x) copying config.ini within the program folder causes administrative bickering, we need a better option :(, I dont want to go full inferno.ini in the users home folder >_< derpmax, something something configurationmanager? yep, that config.ini in program files is not writeable >_< DERP

x) apparently there is a way to call an init script... should look in to that for inferno.bat?

x) set the build option that changes path names...

x) get rid of newline at the start of the csv file

x) for some reason when switching to a different protocol the protocol will sometimes not load properly... it seems to be missing the click?! there seems to be a stupid little window that pops up for just a couple miliseconds... going to try just double clicking the record button...

x) IF CELLS ARE NOT ON THE HEADSTAGE STILL LOAD ALL THE PROTOCOL STUFF OR PCLAMP WILL ERROR

x) split out the functions in inferno.py to their own file so that they can be tested independently

x) Naming consistency: the program itself is Clampex fix this, pClamp is the suite of software
