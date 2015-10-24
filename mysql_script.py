#!/usr/bin/python3

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
#	Stored in [Local] store_file file 								#
#####################################################################

import ConfigParser	
import MySQLdb as mdb
import sys
import logging
import os.path
import os
import time

propertiesFile = 'config.properties'
properties = ConfigParser.ConfigParser()

server_ip = ''
db_name = ''
root_user = ''
root_pwd = ''
databases = []
db_connection = None

SHOW_TABLE_REQ = "SHOW tables"
SHOW_CREATE_TABLE_REQ = "SHOW CREATE TABLE"
SELECT_ALL = "SELECT * FROM"

FORMAT = '%(asctime)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger ("mysql dump")
logger.setLevel(10)

db_connection = None

dump_folder = ''


def connect_to_server (database) :

	global server_ip
	global root_pwd
	global root_user
	global db_connection

	try :
		print "db_connection = mdb.connect(195.154.64.41 "+root_user+", "+root_pwd+", "+database+")"
		db_connection = mdb.connect(server_ip, root_user, root_pwd, database)

		return 0
	except Exception:
		raise
		return 1

#def show_databases ():
#
#def describe_tables (database):
#
#def load_table_data (table):
#
def load_config () :

	global server_ip
	global root_pwd
	global root_user
	global databases
	global dump_folder

	if (os.path.isfile(propertiesFile)) :
		logger.debug('File exists : %s', propertiesFile)
		properties.read(propertiesFile)
		logger.debug('Properties : %s', properties)

		server_ip=properties.get('Server','host')
		logger.debug('Properties : %s', server_ip)

		root_user=properties.get('Server','user')
		logger.debug('Properties : %s', root_user)

		root_pwd=properties.get('Server','pwd')
		logger.debug('Properties : %s', root_pwd)
		
		dump_folder=properties.get('Local','store_folder')
		logger.debug('Properties : %s', dump_folder)
		
		databasenbr = os.popen('cat '+propertiesFile+' | grep db | wc -l').read()

		for i in range(1,int(databasenbr)):
		 	
			databases.append(properties.get('Databases', 'db'+str(i)))
		

		logger.info(databases)
		return 0



def array_to_request_builder(stream, table_structure):

	string_builder = ''
	for lines in stream:
		#For each line = each table





def populate_sql_file(db, listTupleDump, type):
	# listTupleDump : list of tuples returned by SQL request
	# type : 1=TABLE STRUCTURE, 2=DATA

	global dump_folder

	dump_file=None

	if os.path.isdir(dump_folder+'/tbl_struct') :
		if os.path.isdir(dump_folder+'/tbl_data') :



			headerMsg ="""---------------------------------------------\n
							-- MySQL dump script by Spaulding -----------\n
							---------------------------------------------\n
							-- Database : '+db+'\n
							-- Host : '+server_ip+'\n
							---------------------------------------------\n"""

			logger.info(str(len (listTupleDump))+' tables to insert')
			
			if len(listTupleDump) > 0 :
				if len (listTupleDump[0]) == 2 and type == 1:
					
					#### Table structures
					
					logger.debug('Log : '+dump_folder+'/tbl_struct/tbl_struct_'+db+'_'+time.strftime("%Y-%m-%d %H:%M:%S")+'.sql')
					dump_file = open(dump_folder+'/tbl_struct/tbl_struct_'+db+'_'+time.strftime("%Y-%m-%d %H:%M:%S")+'.sql', 'w')
					
					dump_file.write(headerMsg)

					for i in range(0, len(listTupleDump)):
						logger.debug('Writing %s', listTupleDump[i][1])

						dump_file.write(str(listTupleDump[i][1])+'\n;\n\n')

					logger.info('Closing file')
		
					dump_file.close()


					return 0

				elif type == 2:
					#### Data 
					logger.debug('Log : '+dump_folder+'/tbl_data/tbl_data'+db+'_'+time.strftime("%Y-%m-%d %H:%M:%S")+'.sql')
					dump_file = open(dump_folder+'/tbl_data/tbl_data'+db+'_'+time.strftime("%Y-%m-%d %H:%M:%S")+'.sql', 'w')


					print "******************************"
					print listTupleDump
					print "******************************"
					dump_file.write(headerMsg)

					logger.debug('Writing line %s', listTupleDump)
					dump_file.write(listTupleDump[1])


					dump_file.close()

					return 0

				else:
					return 0


		else :
			os.makedirs(dump_folder+'/tbl_data')
			populate_sql_file(db, listTupleDump, type)
	else :

		os.makedirs(dump_folder+'/tbl_struct')
		populate_sql_file(db, listTupleDump, type)



###########################################
## Main ###################################
###########################################
def main() :


	global db_connection
	print "==MySQL Dump=="

	print "Reading config file : "+propertiesFile
	ret = load_config()

	if ret == 0 :
		
		print str(len(databases))+" databases counted !"

		for database in databases :

			print "Config loaded, trying to connect to server "+server_ip+" with user "+root_user
			print "..."

			if connect_to_server(database) == 0 :
				
				print "Connected to "+str(server_ip)+" : "+str(database)

				print database

				#ready = raw_input("Ready to dump ? (y/n)")

			#	if ready == 'y' :

				#Looping over databases
				for database in databases :
					print "Working on database : "+str(database)+" ..."
					print "Saving tables :"
					cursor = db_connection.cursor()

					cursor.execute(SHOW_TABLE_REQ)
					tables = cursor.fetchall()

					#Contains all tables structures
					database_dump = []
					#Contains all data 
					data_dump = []
					for table in tables :

						logger.info("Retrieving table structure for table %s", table[0])
						cursor.execute(SHOW_CREATE_TABLE_REQ+" "+table[0])
						table_structure = cursor.fetchone()

						if len(table_structure) == 2 :
							logger.debug('Table structure : %s', table_structure)
							database_dump.append(table_structure)


						else :
							logger.error('!! Table structure tuple containing '+str(len(table_structure))+' elements')
							sys.exit(1)

						logger.info("Retrieving data for table %s", table[0])

						cursor.execute(SELECT_ALL+' '+table[0])

						table_data = cursor.fetchall()

						data_dump.append((table,table_data))



					populate_sql_file(database, database_dump, 1)
					populate_sql_file(database, data_dump, 2)

				logger.info("Batch return code=0. SUCCESSFUL")

				logger.info("Exiting now ...")
				sys.exit(0)
			#	else :
			#		sys.exit(0)
			else :
				print "Error connectiong to server "+str(connect_to_server(database))
				sys.exit (1)
	else :
		logger.error("Config load failed")
		sys.exit(1)



if __name__ == '__main__' :
	main()
