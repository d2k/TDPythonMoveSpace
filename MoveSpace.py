#!/yourPath/python

##########################################################
### Author: Ulrich Arndt
### Company: data2knowledge Gmbh
### website: www.data2knowledge.de
### First creation date: 02.12.2015
### License:
# The MIT License (MIT)
#
# Copyright (c) 2015 by data2knowledge GmbH, Germany
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##########################################################

import teradata
import argparse
import logging

logger = logging.getLogger(__name__)

###########################################################
# Process the command line information
###########################################################

parser = argparse.ArgumentParser(description='Teradata Create User Script')
parser.add_argument('-l','--logonfile', nargs=1,
                   help='logon file for the user creation')
parser.add_argument('-c','--configfile', nargs=1,
                   help='config file for the user creation')

args = parser.parse_args()

###########################################################
# Set Default config and logon info files in case they are not given at programm call
###########################################################
configfile = ''
if args.configfile:
	configfile = args.configfile[0]
else:
	configfile = './appini/demo.ini'

logonfile = ''
if args.logonfile:
	logonfile = args.logonfile[0]
else:
	logonfile = './dwl/demo.dwl'



############################################################
# Main
###########################################################

############# 
#init udaExec
############# 

udaExec = teradata.UdaExec (userConfigFile=[configfile,logonfile])

session = udaExec.connect(
	method		='rest', 
	system		='${system}',
	username	='${user}', 
	password	='${password}',
	host		='${host}',
	port		='${port}'
	)
	


with session: 

	############# 
	#create db Template
	#############
	size = int(udaExec.config['SizeInGB'])*1024**3
	
	os = '''
select databasename, 
       sum(currentperm) / 1024**3 as currentperm, 
       sum(maxperm) / 1024**3 as maxperm
from dbc.allspaceV
where databasename in (\''''+udaExec.config['FromDB']+'''\',\''''+udaExec.config['ToDB']+'''')
group by 1
order by 1
	'''
	
	print('Current DB Space for From and To DB')
	print('DB\tCurrentPerm\tMaxPerm')
	for row in session.execute(os):
		print("%s:\t%8.2f\t%8.2f" % (row[0],row[1],row[2]))
	
	cdb = '''CREATE DATABASE move_space FROM ''' + udaExec.config['FromDB'] + ''' AS perm='''  + str(size)  
	session.execute(cdb)
	udaExec.checkpoint("DB created")	
	
	g = '''GIVE move_space TO ''' + udaExec.config['ToDB'] 
	session.execute(g)
	udaExec.checkpoint("Give executed")	
	
	ddb = '''DROP DATABASE move_space'''
	session.execute(ddb)
	udaExec.checkpoint("DB dropped")
	
	print('-----------------------------------------')	
	print('\nNEW DB Space for From and To DB')
	print('DB\tCurrentPerm\tMaxPerm')
	for row in session.execute(os):
		print("%s:\t%8.2f\t%8.2f" % (row[0],row[1],row[2]))
		
# Script completed successfully, clear checkpoint
# so it executes from the beginning next time
udaExec.checkpoint()
print('Success')
exit(0)