# TDPythonMoveSpace
Move Space from one TD DB to an other

feel free to donate bitcoin:12kgAUHFUqvG2sQgaRBXFhCwyf9HXdkGud?label=TeradataDev

##Install

clone the repository or download and unzip the zip file

##Configuration

The main configuration is done via three ini files:

* udaexec.ini - contains the main udaexec ini information
* dwl/XXX.dwl - contains the database logon information
* appini/YYY.ini - contains the specific pivot transformation information


###database logon information - dwl/demo.dwl

The database logoninformation requires the following parameter:

* production=True/False
* password=myPassword
* user=myUser
* system=mySystem
* host=myRestServer
* port=myRestServerPort - Standard 1080

### udaexec.ini 

no parameter are expected to be changed

### create user config file (like demo.ini)

* FromDB = sourceDB
* ToDB = targetDB
* SizeInGB = Space to be moved in GB

## program call

example programm calls

python MoveSpace.py -h

result:

usage: MoveSpace.py [-h] [-l LOGONFILE] [-c CONFIGFILE]

Teradata create user programm

optional arguments: -h, --help show this help message and exit -l LOGONFILE, --logonfile LOGONFILE logon file for the user creation -c CONFIGFILE, --configfile CONFIGFILE config file for the user creation

python MoveSpace.py -l dwl/demo.dwl -c appini/demo1.ini
