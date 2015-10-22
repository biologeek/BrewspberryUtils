#!/usr/bin/python

#####################################################################
#	MYSQL server whole dump											#
#*******************************************************************#
#	Version 1.0														#
#	Author XCN														#
#	License Free													#
#-------------------------------------------------------------------#
#	Dumps all MySQL databases available on server					#
#	must be connected as root										#
#																	#
#	Properties files												#
#####################################################################

import ConfigParser	

propertiesFile = './config.properties'
properties = ConfigParser.RawConfigParser()

server_ip = ''
db_name = ''
root_user = ''
root_pwd = ''


def connect_to_server () :


def show_databases ():

def describe_tables (database):

def load_table_data (table):

def load_config () :

	try :
		properties.read(propertiesFile)
	
		server_ip=properties.get('Server','ip_address')
		root_user=properties.get('Server','root_user')
		root_pwd=properties.get('Server','root_pwd')
		return 0
	except Exception:
		return 1

print "==MySQL Dump=="

print "Reading config file : "+propertiesFile

if load_config() == 0 :

	print "Config loaded, trying to connect to server "+server_ip+" with user "+root_user
	print "..."

	if connect_to_server() == 0 :
		
		print "Connected to "+server_ip
	else :
		print "Error connectiong to server"


else :
	
	print "Config load failed"


