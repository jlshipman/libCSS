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
import migrate2
import dictFunc
import archiveFunc
#password="nji9mko0NJI(MKO)"

class TestMigrate2(unittest.TestCase):
 	
	def setUp(self):
		print ""
		print "setUp"
			
	def testlLstCSSFiles(self):
		print "testLstCSSFiles"
		#stage="development"
		stage="production"
		type="nearline"
		#remoteHost="css-10g.larc.nasa.gov"
		#user="jshipman"

		############## variable assignments - begin #####################
		baseAssign="/scripts/nearLine/LIST/baseVariables.txt"
		if stage == "development":
			variableAssign="/scripts/nearLine/LIST/variableAssignDev.txt"
		else:
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
		############## setup log - begin #####################		
		lg=log.log()
		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
		############## setup log - end #####################			
		############## setup log - end #####################
		stage = "development"	
		retObj = migrate2.listCSSFiles (lg, dictVar,stage)
		results = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		print "\t\tresult"
		for r in results:
			print "\t\t\tr:  " + str(r)

# 	def testMigrate(self):
# 		print "testMigrate"
# 		#stage="development"
# 		stage="production"
# 		type="nearline"
# 		#remoteHost="css-10g.larc.nasa.gov"
# 		#user="jshipman"
# 
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
# 						
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 		
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
# 		retObj = migrate2.migrate (lg, mailList, baseAssign, variableAssign, type, remoteHost, user, stage)
# 		results = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tresult"
# 		for r in results:
# 			print "\t\t\tr:  " + str(r)
			

# 	def testCreateListArchives(self):
# 		print "testCreateListArchives"
# 		stage="development"
# 		#stage="production"
# 		type="nearline"
# 		#remoteHost="css-10g.larc.nasa.gov"
# 		#user="jshipman"
# 
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
# 						
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 		
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObj = migrate2.createListArchives(lg, dictVar, type, stage )
# 	
# 		results = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\tresult"
# 		for r in results:
# 			print "\t\t\tr:  " + str(r)

# 			
# 	def testCheckCSS(self):
# 		print "testCheckCSS"
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
# 						
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 		
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObjList = migrate2.createListArchives(lg, dictVar, type, stage )
# 		
# 		pushList = retObjList.getResult()
# 		
# 		retObj=migrate2.checkCSS(lg, dictVar, pushList, type, remoteHost, user, stage )
# 
# 		results = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		error = retObj.getError()
# 		
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		print "\t\terror:   _" + error + "_"	
# 		print "\t\tresult"
# 		for r in results:
# 			print "\t\t\tr:  " + str(r)
			
if __name__ == '__main__':
    unittest.main()
 