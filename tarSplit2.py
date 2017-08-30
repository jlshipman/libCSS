#!/usr/bin/python
try:
	import os, glob, sys, socket
	sys.path.append('lib')
	sys.path.append('libCSS')
	import nearFunctions
	import log
	import fileSize
	import listFunctions
	import fileFunctions
	import directory 
	import fileSize 
	import timeFunc
	import simpleMail
	import dictFunc
	import archiveFunc
	import shutil
	import funcReturn	
	import datetime
	import stringFunctions
	
except ImportError:
	print "missing modules for tarSplit.py"
	sys.exit(1)

def tarSplit (lg, amount, unit, mailList, stage, dictVar, type):
	retObj = funcReturn.funcReturn('Tarsplit')
	now = datetime.datetime.now()
	start = now.strftime("%Y_%m_%d_%H_%M")
	start_time = datetime.datetime.now()
	subject = "FUNCTION Tarsplit    " + start
	message = subject + "\n"
	lg.setPrefix ("Tarsplit")
	lg.info ("FUNCTION tarsplit")		
	lg.info ("\tstage:  " + stage)
	dictVar['prefix']="tarSplit"

	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
		
	mailList = {}
	fromaddr = "admin@" + hostName
	mailList['from_addr'] = fromaddr
	mailList['to_addr'] = toaddr
	############## variable assignments - end #####################	
	
	
	############################# main - begin ###########################
	if os.path.exists(resultsFindings):
		os.unlink(resultsFindings)
	if os.path.exists(splitList):
		os.unlink(splitList)
		
	listSplitTar=listFunctions.listFromFile(splitTarDirListFile)
	for l in listSplitTar:
		if not(os.path.exists ( l )): 
			lg.info ("\tl:  " + l)
			directory.makeDirectoryObj(l)
			own = "ladmin"
			priv = "700"
			directory.setAttributes ( l, own, group1, priv )

	#set amount for split
	splitAmount = str(fileFunctions.convertToBytes ( 100, "GB" ))
	
	#set amount to send
	sendAmount =  str(fileFunctions.convertToBytes ( int(amount), "TB" ))
	output = stringFunctions.tabs(1) +"sendAmount:  " + str(sendAmount)
	message = lg.infoMessage (output, message)

	################################## prepare dir - begin ##################################		
	output = stringFunctions.tabs(1) +"prepare dir"
	message = lg.infoMessage (output, message)

	retObjList = createListJobs( dictVar, type, amount, stage )	
	output = retObjList.getComment()
	message = lg.infoMessage (output, message)
	dirContents = retObjList.getResult()
	#lg.info ("\t\tdirContents:  " + str(dirContents) )
# 	for d in dirContents:
# 		lg.info ("\t\td:  " + d )
	retObjPrepare=prepareDir( dictVar, dirContents, type, stage )
	output = retObjPrepare.getComment()
	message = lg.infoMessage (output, message)
	if retObjPrepare.getRetVal() == 1:
		mailList['subject'] = "createListJobs had an error" 
		mailList['message'] = message + "createListJobs had an error" 
		simpleMail.shortMessage (mailList)
		lg.abort ( "\t\t\tunable to create pushlist" )
		sys.exit(1)
	################################## prepare dir - end ##################################	
		
	################################## split - begin ##################################	
	output = stringFunctions.tabs(1) +"split - begin"
	message = lg.infoMessage (output, message)
	
	retObjList = createListJobs( dictVar, type, amount, stage )
	output = retObjList.getComment()
	message = lg.infoMessage (output, message)
	dirContents = retObjList.getResult()

	retObjTarSplits = createTarSplitsGivenDir ( dictVar, dirContents, sendAmount, splitAmount, type, stage )  
	output = retObjTarSplits.getComment()
	message = lg.infoMessage (output, message)
	
	retDict = retObjTarSplits.getResult()	
	archiveTotal = retDict['archiveTotal']
	totalDuration = retDict['totalDuration']
	retObj.setRetVal(retObjTarSplits.getRetVal())
	
	if totalDuration > 0:
		retObjSize=fileSize.file_Size( archiveTotal )
		gb=retObjSize.getGB()
		gbPerMin = gb / totalDuration
		output = stringFunctions.tabs(3) + "Total gb per min:  " + str(gbPerMin)
		lg.info (output)
		message = message + output + "\n\n"	
	retObjSplitList = createSplitList ( dictVar, type, stage )
	output = retObjSplitList.getComment()
	message = lg.infoMessage (output, message)
	splitTarList=retObjSplitList.getResult()			
	    			
	#create a file of split items, sanPath, cssPath
	fileFunctions.listToFile( splitTarList, splitList)	

	own = "ladmin"
	priv = "770"
	output = "\t\ttempSplit:  " + tempSplit
	lg.info (output)
	message = message + "\n\t" + output + "\n"	

	directory.setAttributes ( tempSplit, own, group1, priv )
	
	################################## split - end ##################################			

	############################# main - end ###########################
	now = datetime.datetime.now()
	end = now.strftime("%Y_%m_%d_%H_%M")
	output = "tarSplit:  end - " + end
	message = lg.infoMessage (output, message)
	
	end_time = datetime.datetime.now()
	timeDict = timeFunc.timeDuration2 (end_time, start_time)
	printHours = timeDict['printHours']
	printMins = timeDict['printMins']
	printSec = timeDict['seconds']
	output = "migration took " + str(printHours) + ":" + str(printMins) + " or " + str(printSec) + " seconds to run"
	message = lg.infoMessage (output, message)
	
	mailList['subject'] = subject
	mailList['message'] = message
	simpleMail.shortMessage (mailList)
	return retObj
	
def createListJobs( dictVar, type, amount, stage):
	retObj = funcReturn.funcReturn('createListJobs')
	output = stringFunctions.tabs(2) + "FUNCTION createListJobs" 
	message = output + "\n"	
	print output
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################	
	dictVar['prefix']="createList"
	#find list in files to archive
	searchList = []
	searchDirectories = scriptDir + searchDirectories
	
	output = stringFunctions.tabs(3) + "type:  " + str(type)
	print output
	message = message + output + "\n"	

	output = stringFunctions.tabs(3) + "searchDirectories:  " + searchDirectories
	print output
	message = message + output + "\n"	
	if stage == "production":
		searchList = listFunctions.listFromFile(searchDirectories)
	elif stage == "other":
		searchList = listFunctions.listFromFile(searchDirectories)
	else:
		searchList = listFunctions.listFromFile(searchDirectories)
	gbAmount = int(amount) * 1000

	output = stringFunctions.tabs(4) + "gbAmount:  "+ str(gbAmount)
	print output
	message = message + output + "\n"	
	#gbAmount = 2500
	totalgb = 0
	#if type == "archiveGraphix":
	if type == "nearLine" or  type == "archiveGraphix":
		#get iterate through list of directories to process
		dirContents = []
		count = len(searchList)
		for d in searchList:
			output =  stringFunctions.tabs(4) + "directory:  "+ d.rstrip()
			print  "\n"	+ output + "\n"	
			message = message + output + "\n"	
			#split on whitespace
			term =d.split()
		
			#get contents of directory
			dirContentsTemp = glob.glob(term[0] + "/*" )
		
			#searches broken down into search with or without exclusions 
			countTerms = len(term)

			for t in dirContentsTemp:
				if t.find("nearLinels") == -1 :
					output =  stringFunctions.tabs(5) + "item:  " + t
					print output
					message = message + output + "\n"
					#if count terms is one add entire directory
					if countTerms == 1:
						sizeRetObj=directory.getDirSize(t)
						amount = sizeRetObj.getResult()
						retObjfileSize=fileSize.file_Size( amount )
						size=retObjfileSize.getSize()
						output = stringFunctions.tabs(4) + "size:  " + str(size)
						print output
						message = message + output + "\n"
						gb=retObjfileSize.getGB()
						totalgb = totalgb + gb
						output = stringFunctions.tabs(4) + "size of archive :  " + str(gb) + " GB"
						print output
						message = message + output + "\n"
						output = stringFunctions.tabs(3) + "total size of all archives :  " + str(totalgb) + " GB"
						print output
						message = message + output + "\n"
						if (gbAmount > totalgb):
							dirContents.append(t)
						else:
							break
					
					#if count term is not one add entire directory except for second term
					else:
						if d.find(term[1]) == -1:
							sizeRetObj=directory.getDirSize(t)
							amount = sizeRetObj.getResult()
							retObjfileSize=fileSize.file_Size( amount )
							size=retObjfileSize.getSize()
							output = stringFunctions.tabs(3) + "size:  " + str(size)
							print output
							message = message + output + "\n"
							gb=retObjfileSize.getGB()
							totalgb = totalgb + gb
							output = stringFunctions.tabs(4) + "size of archive :  " + str(gb) + " GB"
							print output
							message = message + output + "\n"
							output = stringFunctions.tabs(3) + "total size of all archives :  " + str(totalgb) + " GB"
							print output
							message = message + output + "\n"
							if (gbAmount > totalgb):
								dirContents.append(t)
							else:
								break
				
		#remove wildcard entries from list of paths	
		listFunctions.removeValuesList (dirContents, term[0] + "/*" )
	retObj.setComment(message)	
	retObj.setResult(dirContents)
	retObj.setRetVal(0)
	return retObj
	
def prepareDirName( dictVar, d, type, stage ):
	retObj = funcReturn.funcReturn('prepareDirName')
	
	output = stringFunctions.tabs(3) + "FUNCTION prepareDirName" 
	message = output + "\n"	
	print output

	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################	
	dictVar['prefix']="prepareDirName"
	
	output = stringFunctions.tabs(4) + "d:  " + d 
	message = message + output + "\n"	
	print output
	baseOrig = os.path.basename(d)
	dirUpFull = os.path.dirname(d)
	
	#remove offensive char
	base=fileFunctions.removeBadChar2(baseOrig)
	output = stringFunctions.tabs(4) + "baseOrig:  " + baseOrig
	message = message + output + "\n"	
	print output
	output = stringFunctions.tabs(4) + "prepare file and dir start"
	message = message + output + "\n"	
	print output
	output = stringFunctions.tabs(4) + "base remove char:  " + base
	message = message + output + "\n"	
	print output
	
	if type == "nearLine":
		#remove name to CamelCase
		base=fileFunctions.convertNameToCamel (base, "_")
		output = stringFunctions.tabs(4) + "base upper char:  " + base
		message = message + output + "\n"	
		print output
	#compare new name against original
	if base != baseOrig:
		newFullPath = dirUpFull + "/" + base
		output = stringFunctions.tabs(4) + "d:            " + d
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(4) + "newFullPath:  " + newFullPath
		message = message + output + "\n"	
		print output
		retObjDir=directory.mvDir(d, newFullPath)
		retVal = retObjDir.getRetVal()
		if retVal == 1:
			error = retObjDir.getError()
			retObj.setError( retObj.getError() + "\n move dir error:  " + error )
			mailList['subject'] = mailList['message'] = message = message + "unable to rename directory: " +  d 
			simpleMail.shortMessage (mailList)
			lg.abort ( "\tunable to rename directory: " +  d )
			retObj.setRetVal(1)
			return retObj
		output = stringFunctions.tabs(4) + "renamed file"
		message = message + output + "\n"	
		print output
	else:
		newFullPath=d
		
	retObj.setComment(message)	
	retObj.setResult(newFullPath)
	retObj.setRetVal(0)
	return retObj

def prepareDir ( dictVar, dirContents, type, stage ):
	retObj = funcReturn.funcReturn('prepareDir')
	output = stringFunctions.tabs(2) + "FUNCTION prepareDir" 
	message = output + "\n"	
	print output
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################	
	dictVar['prefix']="prepareDir"
	print ("")
	for d in dirContents:	
		#rename directories, removing undesirable characters
		output = stringFunctions.tabs(3) + "prepareDir  d:  " + d
		message = message + output + "\n"	
		print output
		retObjPrepare=prepareDirName( dictVar, d, type, stage )
		output = retObjPrepare.getComment()
		message = message + output + "\n"	
		print output
		if retObjPrepare.getRetVal() == 1:
			output =  "could not rename:  " + d
			message = message + stringFunctions.tabs(2) + output + "\n"
			retObj.setError(output)
			retObj.setRetVal(1)
			return retObj
		else:
			newFullPath = retObjPrepare.getResult() 
		
		priv="775"
		own = "ladmin"
		retObjAtt = directory.setAttributes ( d, own, group1, priv )
		 
	retObj.setComment(message)		
	retObj.setRetVal(0)
	return retObj	
		
def createTarSplits ( dictVar, paraList, type, stage ):
	retObj = funcReturn.funcReturn('createTarSplits')
	output = stringFunctions.tabs(1) + "FUNCTION createTarSplits" 
	message = output + "\n"	
	print output

	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	dictVar['prefix']="createTarSplits"
	############## variable assignments - end #####################	

	
	############## create archive splits - begin #####################
	#resultDict = fileFunctions.makeArchiveSplitReturn (paraList)
	retObj = archiveFunc.tarSplitWrap (paraList)
	retVal = retObj.getRetVal ()
	if retVal == 1:
		print  ("\t\t\terror:  " + retObj.getError())
		subject = "error with tarSplitWrap"
		body = "error with tarSplitWrap \n error:  " + retObj.getError()
		fromaddr = "admin@" + hostName
		subject = hostName +" - " + scriptName
		mailList['message'] = body 
		mailList['subject'] = subject
		simpleMail.shortMessage (mailList)
		sys.exit (1)
	resultDict = retObj.getResult()
	#print str(resultDict)
	############## create archive splits - end #####################	
	
	############## report duration to perform function - begin #####################	
	durationSeconds=resultDict['seconds']
	durationMinutes=durationSeconds / 60
	print  ("\t\t\t%d seconds" % (durationSeconds))
	print  ("\t\t\t%d minutes" % (durationMinutes))
	sizeArchive=resultDict['size']
	retObjSize=fileSize.file_Size( sizeArchive )
	gb=retObjSize.getGB()	
	print  ("\t\t\tsize of archive in bytes:  " + str(sizeArchive))
	print  ("\t\t\tsize of archive in GB:  " + str(gb) + " GB")
	if durationMinutes > 0:
		gbPerMin = gb / durationMinutes
		print  ("\t\t\tgb per min:  " + str(gbPerMin))
	############## report duration to perform function - end #####################	

	resultDict = {'durationSeconds' : durationSeconds, 'sizeArchive' : sizeArchive}
	retObj.setRetVal(0)
	retObj.setResult(resultDict)
	retObj.setComment(message)	
	return retObj
	
def createTarSplitsGivenDir ( dictVar, dirContents, sendAmount, splitAmount,  type, stage ):
	retObj = funcReturn.funcReturn('createTarSplitsGivenDir')
	output = stringFunctions.tabs(2) + "FUNCTION createTarSplitsGivenDir" 
	message = output + "\n"	
	print output
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	dictVar['prefix']="createTarSplits"
	############## variable assignments - end #####################

	splitTarList = []
	archiveTotal = 0
	totalDuration = 0
	totalCountDir = len(dirContents)
	countDir = 0	

	for d in dirContents:
		base = os.path.basename(d)
		dirUpFull = os.path.dirname(d)
		dirUp = os.path.basename(dirUpFull)
		archiveNameFull = tempTar + base + ".tar"
		
		output = stringFunctions.tabs(3) + "tempSplit: "       + tempSplit
		message = message + output + "\n"	
		print output

		output = stringFunctions.tabs(3) + "base: "       + base
		message = message + output + "\n"	
		print output
		
		if type == "archiveGraphix":
			splitFull = tempSplit + "/" + base + ".tar.part-"
			
		if type == "nearLine":
			if stage != "development":
				splitFull = tempSplit + dirUp + "/" + base + ".tar.part-"
			else:
				splitFull = tempSplit + "/" + base + ".tar.part-"
				
		newFullPath = d
		countDir += 1
		output = stringFunctions.tabs(3) + str(countDir) + " of " + str(totalCountDir)
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(4) + base
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(5) + "archiveNameFull: " + archiveNameFull
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(5) + "splitFull: " + splitFull
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(5) + "newFullPath: " + newFullPath
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(5) + "splitAmount: " + splitAmount
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(5) + "dirUp: " + dirUp
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(5) + "tempSplit: " + tempSplit
		message = message + output + "\n"	
		print output
		#remove old split files from holding directory if they exist 
		#fileFunctions.purge(tempSplitFull, splitFull)
		#sizeOfDir = directory.dirSize(newFullPath)
		retObjDirSize= directory.getDirSize(newFullPath)
		sizeOfDir = retObjDirSize.getResult()
		retObjSize=fileSize.file_Size( sizeOfDir )
		gb=retObjSize.getGB()	
		output = stringFunctions.tabs(4) + "size of Directory in GB: " + str(gb)
		message = message + output + "\n"	
		print output
		#estimate of tar
		archiveTotal += sizeOfDir
		
		output = stringFunctions.tabs(4) + "newFullPath        " + newFullPath
		message = message + output + "\n"	
		print output
		#get partial path  i.e.  readyToArchive/blahblah
		replaceString = ""
		output = stringFunctions.tabs(4) + "SANpath        " + SANpath
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(4) + "replaceString        " + replaceString
		message = message + output + "\n"	
		print output
		cssPath = newFullPath.replace(SANpath, replaceString)
		if type == "archiveGraphix":
			base = os.path.basename(cssPath)
			output = stringFunctions.tabs(3) + "base        " + base
			message = message + output + "\n"	
			print output
			dirAlpha = base[0]
			output = stringFunctions.tabs(3) + "dirAlpha        " + dirAlpha
			message = message + output + "\n"	
			print output
			cssPath = "/" + dirAlpha +  "/" + base
			output = stringFunctions.tabs(3) + "cssPath        " + cssPath
			message = message + output + "\n"	
			print output
			
		if sendAmount > archiveTotal:
			paraList = [ archiveNameFull, newFullPath, splitFull, splitAmount ]	
			retObjSplits = createTarSplits ( dictVar, paraList, type, stage )
			resultDict = retObjSplits.getResult()
			#create more accurate accounting of tar size
			archiveTotal -= sizeOfDir
			archiveTotal += resultDict['sizeArchive']
			totalDuration += resultDict['durationSeconds']
			retObjSize=fileSize.file_Size( archiveTotal )
			gb=retObjSize.getGB()
			output = stringFunctions.tabs(3) + "total size of archive in GB:  " + str(gb) + " GB"
			message = message + output + "\n"	
			print output
			durationMinutes=totalDuration / 60
			if durationMinutes > 0:
				gbPerMin = gb / durationMinutes
				output = stringFunctions.tabs(3) + "gb per min:  " + str(gbPerMin)
				message = message + output + "\n"	
				print output
			print  ("")
		else:
			#archiveTotal is bigger than send amount
			retObj.setRetVal(0)
			retObj.setResult(resultDict)
			return retObj

	resultDict = {'archiveTotal' : archiveTotal, 'totalDuration' : totalDuration}

	retObj.setComment(message)		
	retObj.setRetVal(0)
	retObj.setResult(resultDict)
	return retObj
	
def createSplitList (dictVar, type, stage ):
	retObj = funcReturn.funcReturn('createSplitList')
	output = stringFunctions.tabs(2) + "FUNCTION createSplitList" 
	message = output + "\n"	
	print output
	splitTarList = []
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	dictVar['prefix']="createTarSplits"
	############## variable assignments - end #####################
	output = stringFunctions.tabs(3) + "tempSplit:  " + tempSplit
	message = message + output + "\n"	
	print output
	#create list of dir to look through (i.e p2_SD and readyToArchive)
	dirOfDirContents = glob.glob(tempSplit + "*" )
	output = stringFunctions.tabs(4) + "dirOfDirContents:  " + str(dirOfDirContents)
	message = message + output + "\n"	
	print output
	#create list of split tar directories
	output = stringFunctions.tabs(3) + "create list of split tar directories"
	message = message + output + "\n"	
	print output
	dirContents = []
	
	if type == "archiveGraphix":
		dirContentsSplit = dirOfDirContents
		
	if type == "nearLine":
		for d in dirOfDirContents:
			output = stringFunctions.tabs(4) + d
			message = message + output + "\n"	
			print output
			dirContents += glob.glob( d + "/*" )

		print  ("")
		output = stringFunctions.tabs(3) + "create list of tar splits in directories"
		message = message + output + "\n"	
		print output
		countList = len(dirContents)
		output = stringFunctions.tabs(4) + "s:  " + str(countList)
		message = message + output + "\n"	
		print output
		#create list of tar splits in directories
		dirContentsSplit = []
		for s in dirContents:
			countList = len(dirContents)
			output = stringFunctions.tabs(4) + "s:  " + str(countList)
			message = message + output + "\n"	
			print output
			dirContentsSplit += glob.glob( s + "*")
	
	print  ("")
	output = stringFunctions.tabs(3) + "create list to pass to pushCSS"
	message = message + output + "\n"	
	print output
	countList = len(dirContentsSplit)
	output = stringFunctions.tabs(4) + "s:  " + str(countList)
	message = message + output + "\n"	
	print output
	#create list to pass to pushCSS (cssPath, base, baseSplit, newFullPath, cssBackupArchive)
	for s in dirContentsSplit:
		print  ("    ")
		output = stringFunctions.tabs(4) + "s:  " + str(countList)
		message = message + output + "\n"	
		print output
		backupTerm=[]
		baseTarSplit = os.path.basename(s)
		dirUpFull = os.path.basename(baseTarSplit)
		baseNoPrefixList=baseTarSplit.split(".")
		base=baseNoPrefixList[0]
		output = stringFunctions.tabs(4) + "base:  " + base
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(4) + "baseTarSplit:  " + baseTarSplit
		message = message + output + "\n"	
		print output
		replaceString = ""
		newFullPath = dirUpFull + "/" + base
		if type == "nearLine":
			cssPath = base  +  "/" + baseTarSplit
			output = stringFunctions.tabs(5) + "cssPath:        " + cssPath
			message = message + output + "\n"	
			print output
		if type == "archiveGraphix":
			dirAlpha = base[0]
			output = stringFunctions.tabs(5) + "dirAlpha:        " + dirAlpha
			message = message + output + "\n"	
			print output
			cssPath = "/" + dirAlpha +  "/" + base  +  "/" + baseTarSplit
		output = stringFunctions.tabs(5) + "cssPath:        " + cssPath
		message = message + output + "\n"	
		print output
		backupTerm=cssPath.split('/')
		backupCheck=backupTerm[0].strip()
		output = stringFunctions.tabs(5) + "backupCheck:  _" + backupCheck + "_"
		message = message + output + "\n"	
		print output
		output = stringFunctions.tabs(5) + "backup:  _" + backup + "_"
		message = message + output + "\n"	
		print output
		if backupCheck == backup:
			cssBackupArchive=cssBackup
			print  ("")
			output = stringFunctions.tabs(5) + "cssBackup"
			message = message + output + "\n"	
			print output
			
			output = stringFunctions.tabs(5) + "cssBackupArchive:  " + cssBackupArchive
			message = message + output + "\n"	
			print output
			
			noDate=dirWithoutDate(base)
			output = stringFunctions.tabs(5) + "noDate:  " + noDate
			message = message + output + "\n"	
			print output
			
			dirN=os.path.dirname(cssPath)
			cssPath=dirN+ "/" + noDate
			output = stringFunctions.tabs(5) + "dirN:  " + dirN
			message = message + output + "\n"	
			print output
			
			output = stringFunctions.tabs(5) + "cssPath:  " + cssPath
			message = message + output + "\n"	
			print output
			
			sendList = cssPath + " " + base + " " + baseTarSplit + " " +  newFullPath + " " + cssBackupArchive
			output = stringFunctions.tabs(5) + "sendList:  " +  str(sendList)
			message = message + output + "\n"	
			print output
			
			splitTarList.append(sendList)
		else:
			cssBackupArchive=cssArchive
			print  ("")
			output = stringFunctions.tabs(5) + "cssArchive"
			message = message + output + "\n"	
			print output
			
			output = stringFunctions.tabs(5) + "cssPath:  " + cssPath
			message = message + output + "\n"	
			print output
			
			output = stringFunctions.tabs(5) + "base:  " + base
			message = message + output + "\n"	
			print output
			
			output = stringFunctions.tabs(5) + "baseTarSplit:  " + baseTarSplit
			message = message + output + "\n"	
			print output
			
			output = stringFunctions.tabs(5) + "newFullPath:  " + newFullPath
			message = message + output + "\n"	
			print output
			
			output = stringFunctions.tabs(5) + "cssBackupArchive:  " + cssBackupArchive
			message = message + output + "\n"	
			print output

			sendList = cssPath + " " + base + " " + baseTarSplit + " " +  newFullPath + " " + cssBackupArchive
			output = stringFunctions.tabs(5) + "sendList" + str(sendList)
			message = message + output + "\n"	
			print output
			
			splitTarList.append(sendList)
			
	retObj.setComment(message)					
	retObj.setRetVal(0)
	retObj.setResult(splitTarList)
	return retObj

	
