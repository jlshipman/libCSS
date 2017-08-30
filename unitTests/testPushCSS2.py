#!/usr/bin/python	
import unittest
import os, sys, socket
import subprocess
import re


curDir = os.path.dirname(os.path.realpath(__file__))
print curDir
sys.path.append('../../lib')
sys.path.append('../../libCSS')
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
curDir=os.getcwd()
import remoteFunc
import fileFunctions
import comWrap
import log
import pushCSS2
import dictFunc
import fileSize
#password="nji9mko0NJI(MKO)"
password=""
class TestPushCSS2(unittest.TestCase):
 	
	def setUp(self):
		print ""
		print "setUp"	

# 	def testPushCSS2(self):	
# 		print "testPushCSS2"
# 		stage="development"
# 		#stage="production"
# 		type="nearline"
# 		#remoteHost="css-10g.larc.nasa.gov"
# 		#user="jshipman"
# 		############## variable assignments - begin #####################
# 		baseAssign="/scripts/nearLine/LIST/baseVariables.txt"
# 		if stage == "development":
# 			variableAssign="/scripts/nearLine/LIST/variableAssignDev.txt"
# 		else:
# 			variableAssign="/scripts/nearLine/LIST/variableAssign.txt"
# 		baseVar = dictFunc.fileToDict(baseAssign, ",")
# 		dictVar = dictFunc.fileToDict(variableAssign, "#")
# 		sizeOfBaseDict = len (baseVar)
# 		for x in range(0, sizeOfBaseDict):
# 			for (n, v) in dictVar.items():
# 				var = dictVar[n]
# 				for (key, value) in baseVar.items():
# 					searchTerm="<"+str(key)+">"
# 					retVal=var.find(searchTerm)
# 					if retVal != -1:
# 						newString = var.replace(searchTerm, value)
# 						dictVar[n]=newString	
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################	
# 		############## mail assignments - begin #####################	
# 		hostName=socket.gethostname()
# 		fromaddr = "admin@" + hostName
# 		mailList = {}
# 		mailList['from_addr'] = fromaddr
# 		mailList['to_addr'] = toaddr
# 		############## mail assignments - end #####################	
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObj=pushCSS2.pushCSS2(lg, mailList, dictVar, type, stage, remoteHost, user)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	

# 	def testRemoteMkdirMail(self):	
# 		print "testRemoteMkdirMail"
# 		stage="development"
# 		type="nearline"
# 		remoteHost="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		#password=""
# 		cssDir="/mss/js/jshipman/testing"
# 		############## variable assignments - begin #####################
# 		baseAssign="/scripts/nearLine/LIST/baseVariables.txt"
# 		variableAssign="/scripts/nearLine/LIST/variableAssign.txt"
# 		baseVar = dictFunc.fileToDict(baseAssign, ",")
# 		dictVar = dictFunc.fileToDict(variableAssign, "#")
# 		sizeOfBaseDict = len (baseVar)
# 		for x in range(0, sizeOfBaseDict):
# 			for (n, v) in dictVar.items():
# 				var = dictVar[n]
# 				for (key, value) in baseVar.items():
# 					searchTerm="<"+str(key)+">"
# 					retVal=var.find(searchTerm)
# 					if retVal != -1:
# 						newString = var.replace(searchTerm, value)
# 						dictVar[n]=newString
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################	
# 		############## mail assignments - begin #####################	
# 		hostName=socket.gethostname()
# 		fromaddr = "admin@" + hostName
# 		mailList = {}
# 		mailList['from_addr'] = fromaddr
# 		mailList['to_addr'] = toaddr
# 		############## mail assignments - end #####################	
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObj=pushCSS2.remoteMkdirMail (lg, mailList, remoteHost, user, cssDir, stage, password)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"			
	
	def testRemotePutFileMail(self):	
		print "testRemotePutFileMail"
		stage="development"
		type="nearline"
		remoteHost="css-10g.larc.nasa.gov"
		user="jshipman"
		cssDir="/mss/js/jshipman"
		localFullPath="/scripts/nearLine/libCSS/unitTests/TEMP/txtfile_4_18_9_36.png"
		totalSizeArchive = 0
		totalSecArchive = 0
		############## variable assignments - begin #####################
		baseAssign="/scripts/nearLine/LIST/baseVariables.txt"
		variableAssign="/scripts/nearLine/LIST/variableAssign.txt"
		baseVar = dictFunc.fileToDict(baseAssign, ",")
		dictVar = dictFunc.fileToDict(variableAssign, "#")
		sizeOfBaseDict = len (baseVar)
		for x in range(0, sizeOfBaseDict):
			for (n, v) in dictVar.items():
				var = dictVar[n]
				for (key, value) in baseVar.items():
					searchTerm="<"+str(key)+">"
					retVal=var.find(searchTerm)
					if retVal != -1:
						newString = var.replace(searchTerm, value)
						dictVar[n]=newString
		for (n, v) in dictVar.items():
			exec('%s=%s' % (n, repr(v)))	
		############## variable assignments - end #####################	
		############## mail assignments - begin #####################	
		hostName=socket.gethostname()
		fromaddr = "admin@" + hostName
		mailList = {}
		mailList['from_addr'] = fromaddr
		mailList['to_addr'] = toaddr
		############## mail assignments - end #####################	
		############## setup log - begin #####################		
		lg=log.log()
		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
		############## setup log - end #####################	
		retObj=pushCSS2.remotePutFileMail (lg, mailList, remoteHost, user, cssDir, localFullPath, stage, password)
		results = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		print "\t\tresult:  _" + str(results)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		fileProperties=results['fileProperties']		
		sizeArchive = int(fileProperties['size'])
		durationSeconds = results['seconds']
		totalSizeArchive += sizeArchive
		totalSecArchive += durationSeconds
		totalMinArchive=totalSecArchive / 60
		lg.info ("")			
		lg.info ("\t\tTotal Archive Stats")
		lg.info ("\t\t\t%d seconds" % (totalSecArchive))
		lg.info ("\t\t\t%d minutes" % (totalMinArchive))
		lg.info ("\t\t\tsize of pushed data in bytes:  %d" % (totalSizeArchive))  			
		retObjSize=fileSize.file_Size( totalSizeArchive )
		gb=retObjSize.getGB()
		lg.info ("\t\t\tsize of pushed dat: bytes:  " + str(totalSizeArchive))
		lg.info ("\t\t\tsize of pushed data:  " + str(gb) + " GB")
		
# 	def testCreateTarSplitList(self):
# 		print "testCreateTarSplitList"
# 		stage="development"
# 		type="nearline"
# 		
# 		############## variable assignments - begin #####################
# 		baseAssign="/scripts/nearLine/LIST/baseVariables.txt"
# 		variableAssign="/scripts/nearLine/LIST/variableAssign.txt"
# 		baseVar = dictFunc.fileToDict(baseAssign, ",")
# 		dictVar = dictFunc.fileToDict(variableAssign, "#")
# 		sizeOfBaseDict = len (baseVar)
# 		for x in range(0, sizeOfBaseDict):
# 			for (n, v) in dictVar.items():
# 				var = dictVar[n]
# 				for (key, value) in baseVar.items():
# 					searchTerm="<"+str(key)+">"
# 					retVal=var.find(searchTerm)
# 					if retVal != -1:
# 						newString = var.replace(searchTerm, value)
# 						dictVar[n]=newString
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 		
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObj=pushCSS2.createTarSplitList(lg, dictVar, type, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
		
#  	def testRemotePutCKMail(self):	
# 		print "testRemotePutCKMail"
# 		stage="development"
# 		type="nearline"
# 		remoteHost="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		cssDir="/mss/js/jshipman"
# 		localFullPath="/scripts/nearLine/lib/unitTests/TEMP/txtfile_3_18_9_36"
# 		############## variable assignments - begin #####################
# 		baseAssign="/scripts/nearLine/LIST/baseVariables.txt"
# 		variableAssign="/scripts/nearLine/LIST/variableAssign.txt"
# 		baseVar = dictFunc.fileToDict(baseAssign, ",")
# 		dictVar = dictFunc.fileToDict(variableAssign, "#")
# 		sizeOfBaseDict = len (baseVar)
# 		for x in range(0, sizeOfBaseDict):
# 			for (n, v) in dictVar.items():
# 				var = dictVar[n]
# 				for (key, value) in baseVar.items():
# 					searchTerm="<"+str(key)+">"
# 					retVal=var.find(searchTerm)
# 					if retVal != -1:
# 						newString = var.replace(searchTerm, value)
# 						dictVar[n]=newString
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################	
# 		############## mail assignments - begin #####################	
# 		hostName=socket.gethostname()
# 		fromaddr = "admin@" + hostName
# 		mailList = {}
# 		mailList['from_addr'] = fromaddr
# 		mailList['to_addr'] = toaddr
# 		############## mail assignments - end #####################	
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObj=pushCSS2.remotePutCKMail (lg, mailList, remoteHost, user, cssDir, localFullPath, stage, password)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"			
		
		

if __name__ == '__main__':
    unittest.main()
 