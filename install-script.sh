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


# Valeurs de retour #
RET_OK=0
RET_ABORT=64

# Variables d\'environnement #

TOMCAT_DIR=/opt/tomcat

JDK8_PACKAGE=oracle-java8-jdk
JRE8_PACKAGE=oracle-java8-jre
JAVA8INSTALLER_PACKAGE=oracle-java8-installer

JDK7_PACKAGE=oracle-java7-jdk
JRE7_PACKAGE=oracle-java7-jre
JAVA7INSTALLER_PACKAGE=oracle-java7-installer




#Java install #


echo "*******************************************************"
echo "*		Java/tomcat install script 						"
echo "*														"
echo "*-----------------------------------------------------"
echo "*												"
echo "*												"
echo "*												"

RES_JAVA=dpkg-query -l | grep "$JAVA8INSTALLER_PACKAGE" | wc -l
if [ "$RES_JAVA" -gt "0" ]
	then

	echo "*		$JAVA8INSTALLER_PACKAGE exists					"
else 
	echo "*		$JAVA8INSTALLER_PACKAGE does not exist			"
fi



