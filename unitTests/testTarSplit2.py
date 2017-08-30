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
import tarSplit2
import dictFunc
import archiveFunc

class TestTarSplit2(unittest.TestCase):
 	
	def setUp(self):
		print ""
		print "setUp"	

	def testTarSplit(self):
		print "testTarSplit"
		stage="development"
		#stage="production"
		type="nearline"
		
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
		amount = 2
		unit = "TB"

		retObj=tarSplit2.tarSplit (lg, amount, unit, mailList, stage, baseAssign, dictVar)
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
				
# 	def testCreateSplitList(self):
# 		print "testCreateSplitList"
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
# 						
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 
# 
# 		retObj=tarSplit2.createSplitList (lg, dictVar, type, stage )
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
		
# 	def testCreateTarSplitsGivenDir(self):
# 		print "testCreateTarSplitsGivenDir"
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
# 						
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 		
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObjList = tarSplit2.createListJobs(lg, dictVar, type, stage )
# 		dirContents = retObjList.getResult()
# 		
# 		#set amount for split
# 		splitAmount = str(fileFunctions.convertToBytes ( 100, "GB" ))
# 		
# 		#set amount to send
# 		objRetBytes =  fileFunctions.convertToBytes2 ( 2, "TB" )
# 		sendAmount = objRetBytes.getResult()
# 
# 		print "\t\tcreateTarSplitsGivenDir"
# 		retObj=tarSplit2.createTarSplitsGivenDir (lg, dictVar, dirContents, sendAmount, splitAmount,  type, stage )
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
	
# 	def testCreateListJobs(self):
# 		print "testCreateListJobs"
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
# 						
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 		
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		retObj=tarSplit2.createListJobs(lg, dictVar, type, stage)
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
# 				
# 	def testPrepareDirName(self):
# 		print "testPrepareDirName"
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
# 					
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 	
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		
# 		############## mail assignments - begin #####################	
# 		hostName=socket.gethostname()
# 		fromaddr = "admin@" + hostName
# 		mailList = {}
# 		mailList['from_addr'] = fromaddr
# 		mailList['to_addr'] = toaddr
# 		############## mail assignments - end #####################	
# 
# 		fullPathLists = ['Volumes/videoSAN/Temp/Split/nearLine/readyToArchive/6945_   spaces ','/Volumes/videoSAN/Temp/Split/nearLine/readyToArchive/6967_YagerRunwayFrictionTests','/Volumes/videoSAN/Temp/Split/nearLine/readyToArchive/6982_NilesB1215MishapVideo']
# 		for d in fullPathLists:
# 			print "d:  " + d
# 			dict=archiveFunc.archivePrep (lg, d, tempSplit)
# 			result = dict['retVal']
# 			if result == 0:
# 				path=dict['path']
# 				baseOrig=dict['baseOrig']
# 				dirUpFull=dict['dirUpFull']
# 				dirUp=dict['dirUp']
# 				tempSplitFull=dict['tempSplitFull']
# 				comment=dict['comment']
# 				command=dict['command']
# 				sendDict = {'d' : d, 'baseOrig' : baseOrig, 'dirUpFull': dirUpFull}
# 				retObj=tarSplit2.prepareDirName(lg, mailList, sendDict, d, type, stage )
# 				result = retObj.getResult()
# 				retVal = retObj.getRetVal()
# 				comment = retObj.getComment()
# 				stdout = retObj.getStdout()
# 				stderr = retObj.getStderr()
# 				found = retObj.getFound()
# 				remed = retObj.getRemed()
# 				print "\t\tresult:  _" + str(result)  + "_"
# 				print "\t\tretVal:  _" + str(retVal)  + "_"
# 				print "\t\tcomment: _" + comment + "_"
# 				print "\t\tstdout:  _" + stdout + "_"
# 				print "\t\tstderr:  _" + stderr + "_"
# 				print "\t\tremed:   _" + remed + "_"
# 				print "\t\tfound:   _" + str(found) + "_"	
# 				print ""
# 			else:
# 				print "\t\tThere is a problem with archivePrep"
# 		
# 	def testPrepareDir(self):
# 		print "testPrepareDir"
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
# 					
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 	
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		
# 		############## mail assignments - begin #####################	
# 		hostName=socket.gethostname()
# 		fromaddr = "admin@" + hostName
# 		mailList = {}
# 		mailList['from_addr'] = fromaddr
# 		mailList['to_addr'] = toaddr
# 		############## mail assignments - end #####################		
# 		
# 		retObjList = tarSplit2.createListJobs(lg, dictVar, type, stage )
# 		dirContents = retObjList.getResult()
# 
# 		retObj = tarSplit2.prepareDir(lg, mailList, dictVar, dirContents, type, stage )
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
# 		
# 	def testCreateTarSplits(self):
# 		print "testCreateTarSplits"
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
# 					
# 		for (n, v) in dictVar.items():
# 			exec('%s=%s' % (n, repr(v)))	
# 		############## variable assignments - end #####################
# 	
# 		############## setup log - begin #####################		
# 		lg=log.log()
# 		lg.setData2(prefix, "myLogger", "/scripts/nearLine/libCSS/unitTests/TEMP/LOG")
# 		############## setup log - end #####################	
# 		
# 		############## mail assignments - begin #####################	
# 		hostName=socket.gethostname()
# 		fromaddr = "admin@" + hostName
# 		mailList = {}
# 		mailList['from_addr'] = fromaddr
# 		mailList['to_addr'] = toaddr
# 		############## mail assignments - end #####################		
# 		d = "/Volumes/videoSAN/readyToArchive/6980_JonesCalorieCount3162015"
# 		base = os.path.basename(d)
# 		dirUpFull = os.path.dirname(d)
# 		dirUp = os.path.basename(dirUpFull)
# 		archiveNameFull = tempTar + base + ".tar"
# 		splitFull = tempSplit + dirUp + "/" + base + ".tar.part-"
# 		newFullPath = d
# 		splitAmount = str(fileFunctions.convertToBytes ( 100, "GB" ))
# 		lg.info ("\t\t\tarchiveNameFull: " + archiveNameFull)
# 		lg.info ("\t\t\tsplitFull: "       + splitFull)
# 		lg.info ("\t\t\tnewFullPath: "     + newFullPath)
# 		lg.info ("\t\t\tsplitAmount: "     + splitAmount)
# 		
# 		paraList = [ archiveNameFull, newFullPath, splitFull, splitAmount ]	
# 		retObj = tarSplit2.createTarSplits(lg, dictVar, paraList, type, stage )
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
 