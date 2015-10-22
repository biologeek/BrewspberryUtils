#!/bin/bash

#*******************************************************************#
# 	install-script.sh								v0.1			#
#-------------------------------------------------------------------#
#	Version	|	Date	|	Author	|			Comments			#			
#-------------------------------------------------------------------#
#		0.1	| 20151018	|	XCN		|								#	
#-------------------------------------------------------------------#
#			| 			|			|								#	
#-------------------------------------------------------------------#
#			| 			|			|								#	
#-------------------------------------------------------------------#
#*******************************************************************#
#	Installation of Java / Tomcat environment 						#
#*******************************************************************#


# Return values #
RET_OK=0
RET_ABORT=64

# ENV Variables  #

TOMCAT_DIR=/opt/tomcat export TOMCAT_DIR
JAVA_DIR=/usr/bin export JAVA_DIR

JAVA_EXEC=$JAVA_DIR/java export JAVA_EXEC

# Java Versions
JDK8_PACKAGE=oracle-java8-jdk
JRE8_PACKAGE=oracle-java8-jre
JAVA8INSTALLER_PACKAGE=oracle-java8-installer

JDK7_PACKAGE=oracle-java7-jdk
JRE7_PACKAGE=oracle-java7-jre
JAVA7INSTALLER_PACKAGE=oracle-java7-installer

# Tomcat vars #

TOMCAT_URL=http://www.us.apache.org/dist/tomcat/tomcat-8/v8.0.27/bin/apache-tomcat-8.0.27.tar.gz



# Java install #


echo "*******************************************************"
echo "*		Java/tomcat install script 						"
echo "*														"
echo "*-----------------------------------------------------"
echo "*												"
echo "*												"
echo "*												"

RES_JAVA8=`dpkg-query -l | grep "$JAVA8INSTALLER_PACKAGE" | wc -l`
RES_JAVA7=`dpkg-query -l | grep "$JAVA7INSTALLER_PACKAGE" | wc -l`
if [ "$RES_JAVA8" -gt 0 ]
	then

	echo "** Java installed !"
	echo `java -version`
	echo "** java packages : `dpkg-query -l | grep "java"`"
elif [ "$RES_JAVA7" -gt 0 ]
	then
	
	echo "** Java installed !"
	echo `java -version`
	echo "** java packages : `dpkg-query -l | grep "java"`"
	
else 
	echo "** $JAVA8INSTALLER_PACKAGE does not exist"
	read -p "** Install Java (y/n) ?" ANS1
	
	case $ANS1 in
	
		y ) 
		
		echo "Which environment ?"
		echo "1- OpenJDK"
		echo "2- Oracle"
		read -p "? " JDK
		
		case JDK in
		
			1 )
			
			
			;;
			2 )
				
				
				echo "** adding repository ppa:webupd8team/java"
				sudo apt-add-repository ppa:webupd8team/java
				
				if [ $? = 0 ]
				then
					echo "** Repo complete !"
				else
					echo "!!! Repo failed !!! return code : $?"
					exit $RET_ABORT
				fi
					
					
				echo "** updating"
				sudo apt-get update
				if [ $? = 0 ]
				then
					echo "** Update complete !"
				else
					echo "!!! Update failed !!! return code : $?"
					exit $RET_ABORT
				fi
					
				echo "** installing oracle-java8-installer"
				sudo apt-get install oracle-java8-installer
				
				if [ $? = 0 ]
				then
					echo "** Install complete !"
				else
					echo "!!! Install failed !!! return code : $?"
					exit $RET_ABORT
				fi
			
			
			;;
		esac
		;;
		
		n )
		
			exit $RET_OK
		;;
		
	esac
	


	###### As Java is not installed how could there be a server
	read -p "Want to install a server (y/n) ?" ANS2

	case $ANS2 in
	
		y ) 
		
		echo "Which one ?"
		echo "1- Tomcat "
		read -p "? " SERVER

		case $SERVER in 

			1 )
	
				cd /opt
				sudo mkdir tomcat8
				sudo chmod 775 -R tomcat8

				cd tomcat8
				wget $TOMCAT_URL
				tar xzf apache-tomcat-8.0.27.tar.gz ../tomcat8

				echo "export CATALINA_HOME=\"/opt/tomcat\"" >> ~/.bashrc
				source ~/.bashrc

				echo "Tomcat 8 install complete"

			;;


fi