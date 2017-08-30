#!/usr/bin/python
try:
	import socket, os, sys, glob
	sys.path.append('lib')
	import listFunctions
	import fileFunctions
	import masStoreFunc
	import comWrap	
	import simpleMail
	import dictFunc
	import shutil
	import funcReturn
	import remoteFunc
	import time
	import datetime
	import stringFunctions
	import timeFunc
	
except ImportError:
	print "missing modules for migrate.py"
	sys.exit(1)
	
def migrate (lg, mailList, dictVar,  type, remoteHost, user, stage="production"):
	retObj = funcReturn.funcReturn('migrate')
	now = datetime.datetime.now()
	start_time = datetime.datetime.now()
	start = now.strftime("%Y_%m_%d_%H_%M")
	subject = "FUNCTION migration    " + start
	message = subject + "\n"
	lg.info ("FUNCTION migrate")
	lg.setPrefix ("migrate")	
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################
	hostName=socket.gethostname()
	
	############################# main - begin ###########################
	#get info from file
	if os.path.exists(onTapeFile):
		os.unlink(onTapeFile)
	if os.path.exists(onTapeSearchFile):
		os.unlink(onTapeSearchFile)	
		
	#get list of archived files
	retOjb = createListArchives(lg, dictVar, type, stage )
	if retOjb.getRetVal() == 0:
		retDict = retOjb.getResult()
		message = message + retDict['message']
		pushList = retDict['pushList']
	else:
		mailList['subject'] = "unable to create pushlist" 
		mailList['message'] = "unable to create pushlist" 
		simpleMail.shortMessage (mailList)
		lg.abort ( "\t\t\tunable to create pushlist" )
		sys.exit(1)
	
	retOjb = checkCSS(lg, dictVar, pushList, type, remoteHost, user, stage )
	output = stringFunctions.tabs(1) + "checkCSS - retOjb.getRetVal(): " + str(retOjb.getRetVal())
	message = lg.infoMessage (output, message)
	
	if retOjb.getRetVal() == 0:
		retDict = retOjb.getResult()
		onTapeList = retDict['onTapeList'] 
		onCacheList = retDict['onCacheList']
		message = message + retDict['message']
		lg.info ("retDict['message']:  "  + retDict['message'])
	else:
		mailList['subject'] = "unable to check CSS" 
		mailList['message'] = message + retDict['message']
		simpleMail.shortMessage (mailList)
		lg.abort ( "\t\t\tunable to check CSS" )
		sys.exit(1)
		

	############################# determine if we can move or delete files - begin ########################### 		
	fileFunctions.listToFile( onTapeList, onTapeFile )
	fileFunctions.listToFile( onCacheList, onCacheFile )	
	for items in onTapeList:
		(a, b, c) = items.split(",")
		localcssPath = a.rstrip()
		archiveName = b.rstrip()
		fullPathLocalSplitPath = c.rstrip()
		baseName = os.path.basename(localcssPath)
		#lg.info ("\t\titems:  " + items)
		output = stringFunctions.tabs(1) + "Determine if we can move or delete files "
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(1) + "Delete split archive:  " + fullPathLocalSplitPath
		message = lg.infoMessage (output, message)

		output = stringFunctions.tabs(2) + "archiveNameSplitName:  " + archiveName
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "localcssPath:  " + localcssPath
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "baseName:  " + baseName
		message = lg.infoMessage (output, message)

		#delete archive
		output = stringFunctions.tabs(2) + "fullPathLocalSplitPath:  " + fullPathLocalSplitPath
		message = lg.infoMessage (output, message)
						
		if fileFunctions.fileExist(fullPathLocalSplitPath):
			try:
				fileFunctions.fileDelete(fullPathLocalSplitPath)
			except Exception:
				output = "Problem deleting:  " + fullPathLocalSplitPath 
				message = lg.warnMessage (output, message)
				
		if (type == "archive"):
			info ("")
			output = stringFunctions.tabs(3) + "archive "
			message = lg.infoMessage (output, message)
			searchList = fileFunctions.listFromFile(searchDirectories)
			for d in searchList:	
				output = stringFunctions.tabs(3) + "directory:  "+ d.rstrip()
				message = lg.infoMessage (output, message)
				#split on whitespace
				term =d.split()
				baseName=os.path.basename(localcssPath)
				oldFullPath =  d.rstrip() + "/" + baseName
				output = stringFunctions.tabs(3) + "oldFullPath:  " + oldFullPath
				message = lg.infoMessage (output, message)
				if os.path.exists(oldFullPath):
					output = stringFunctions.tabs(3) + "old path exists"
					message = lg.infoMessage (output, message)
					
					newFullPath =  SANpath + localcssPath
					output = stringFunctions.tabs(3) + "newFullPath:  " + newFullPath
					message = lg.infoMessage (output, message)
						
					try:
						shutil.move(oldFullPath, newFullPath)
					except Exception as e:
						print e
						mailList['subject'] = "unable to move: " + oldFullPath
						mailList['message'] = "shutil move error:  " + oldFullPath
						simpleMail.shortMessage (mailList)
						lg.abort ( "\t\t\tunable to move: " + oldFullPath)
						sys.exit(1)
				else:
					output = stringFunctions.tabs(3) + "old path DOES NOT exists"
					message = lg.infoMessage (output, message)
		else:
			lg.info ("")
			output = stringFunctions.tabs(3) + type
			message = lg.infoMessage (output, message)
			if type == "nearLine":
				fullPathDirectory =  SANpath + localcssPath
				output = stringFunctions.tabs(3) + "fullPathDirectory:  " + fullPathDirectory
				message = lg.infoMessage (output, message)
				
				resultDirectoryDelete = comWrap.comWrapDelete (fullPathDirectory)
				if resultDirectoryDelete == 1:
					output = stringFunctions.tabs(3) + "Problem deleting directory:  " + fullPathLocalSplitPath 
					message = lg.warnMessage (output, message)
				lg.info ("")
				
			if type == "archiveGraphix":
				fullPathDirectory =  localcssPath
				output = stringFunctions.tabs(3) + "fullPathDirectory:  " + fullPathDirectory
				message = lg.infoMessage (output, message)
			lg.info ("")

	############################# determine if we can move or delete files - end ########################### 		

	if type == "archiveGraphix":
		sys.exit(1)
	now = datetime.datetime.now()
	end = now.strftime("%Y_%m_%d_%H_%M")
	output = "migration:  end - " + end
	message = lg.infoMessage (output, message)
	end_time = datetime.datetime.now()
	timeDict = timeFunc.timeDuration2 (end_time, start_time)
	printHours = timeDict['printHours']
	printMins = timeDict['printMins']
	printSec = timeDict['seconds']
	output = "migration took " + str(printHours) + ":" + str(printMins) + " or " + str(printSec) + " seconds to run"
	message = lg.infoMessage (output, message)
	
	retObj=listCSSFiles(lg, dictVar, stage="production")
	retDict = retOjb.getResult()
	output = retDict['message']
	print output
	message = lg.infoMessage (output, message)

	mailList['subject'] = subject
	mailList['message'] = message
	simpleMail.shortMessage (mailList)
	############################# main - end ###########################
	retObj.setRetVal(0)
	return retObj
	
def listCSSFiles(lg, dictVar, stage="production"):
	message = "FUNCTION:  listCSSFiles \n"
	print "listCSSFiles"
	#created list of files in a directory on CSS
	retObj = funcReturn.funcReturn('listCSSFiles')
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################	
	MSSUSER="jshipman"
	os.putenv("MSSUSER", MSSUSER)
	os.putenv("MSSHOST", "css-10g")
	
		#hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remotePathDst="/mss/js/jshipman/archive1"
# 		localPathSrc="/scripts/nearLine/lib/unitTests/TEMP/txtfile_3_18_9_36"
# 		retObj=remoteFunc.putFileDirCheck(hostname, user, remotePathDst, localPathSrc, stage, password)
	hostname=socket.gethostname()
	if stage == "development":
		lsFile = "/scripts/nearLine/" + lsFile

	lsFileList = []
 	lsFileList = fileFunctions.listFromFile(lsFile)
	if stage == "development":
		archiveFile = "/scripts/nearLine/" + archiveFile

	output = stringFunctions.tabs(1) + "archiveFile "
	print output
	message = lg.infoMessage (output, message)
	with open(archiveFile, 'r') as f:
		archive = f.readline().rstrip()
		output = stringFunctions.tabs(2) + "archive:  " + archive
		print output
		message = lg.infoMessage (output, message)
	f.close()	
	
	output = stringFunctions.tabs(1) + "lsFileList "
	message = lg.infoMessage (output, message)
	for item in lsFileList:
		term =item.rstrip().split()
		output = stringFunctions.tabs(2) + "item:  " + item
		print output
		message = lg.infoMessage (output, message)
		output = stringFunctions.tabs(1) + "Determine if we can move or delete files "
		listFile = term[0] + "/nearLinels.txt"
		if os.path.exists(listFile):
			os.unlink(listFile)	
		cssDir=archive + "/" + term[1]
		output = stringFunctions.tabs(2) + "cssDir:  " + cssDir
		message = lg.infoMessage (output, message)
		resultDic = masStoreFunc.masDirListing ( cssDir, tempScriptDir )
		print "resultDic['retVal']:  " + str(resultDic['retVal'] )
		if resultDic['retVal'] == 0:
			listing = resultDic['listDirContents']
			fileFunctions.listToFile( listing, listFile)
		else:
			error = resultDic['error'] + " " + resultDic['error2']
			print error
			message = message + error
			retObj.setResult(message)
			retObj.setError("listCSSFiles: Unalbe to create ls of CSS files")
			retObj.setRetVal(1)
			return retObj
	
	retObj.setResult(message)
	retObj.setRetVal(0)
	return retObj
	
def removeTransferFile(lg, dictVar, onTape, type):
	message = "FUNCTION:  removeTransferFile \n"
	retObj = funcReturn.funcReturn('removeTransferFile')
	
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################	
	for items in onTape:
		(a, b, c) = items.split(",")
		localcssPath = a.rstrip()
		archiveName = b.rstrip()
		fullPathLocalSplitPath = c.rstrip()
		baseName = os.path.basename(localcssPath)
		#lg.info ("\t\titems:  " + items)
		output = stringFunctions.tabs(1) + "Determine if we can move or delete files "
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(1) + "Delete split archive:  " + fullPathLocalSplitPath
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "archiveNameSplitName:  " + archiveName
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "localcssPath:  " + localcssPath
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "baseName:  " + baseName
		message = lg.infoMessage (output, message)
				
		#delete archive
		output = stringFunctions.tabs(2) + "fullPathLocalSplitPath:  " + fullPathLocalSplitPath
		message = lg.infoMessage (output, message)
		resultArchiveDelete = comWrap.fileDeleteReturn(fullPathLocalSplitPath)
		if resultArchiveDelete == 1:
			output = "Problem deleting:  " + fullPathLocalSplitPath
			message = lg.warnMessage (output, message)		
		if (type == "archive"):
			output = stringFunctions.tabs(3) + "archive"
			message = lg.infoMessage (output, message)
			searchList = fileFunctions.listFromFile(searchDirectories)
			for d in searchList:	
				output = stringFunctions.tabs(3) + "directory:  "+ d.rstrip()
				message = lg.infoMessage (output, message)
				
				#split on whitespace
				term =d.split()
				baseName=os.path.basename(localcssPath)
				oldFullPath =  d.rstrip() + "/" + baseName
				output = stringFunctions.tabs(3) + "oldFullPath:  " + oldFullPath
				message = lg.infoMessage (output, message)
				
				if os.path.exists(oldFullPath):
					output = stringFunctions.tabs(3) + "old path exists"
					newFullPath =  SANpath + localcssPath
					output = stringFunctions.tabs(3) + "newFullPath:  " + newFullPath
					message = lg.infoMessage (output, message)
					try:
						shutil.move(oldFullPath, newFullPath)
					except Exception as e:
						print e
						mailList['subject'] = "unable to move: " + oldFullPath
						mailList['message'] = message + "shutil move error:  " + oldFullPath
						simpleMail.shortMessage (mailList)
						lg.abort ( "\t\t\tunable to move: " + oldFullPath)
						sys.exit(1)
				else:
					output = stringFunctions.tabs(3) + "old path DOES NOT exists"
					message = lg.infoMessage (output, message)
		else:
			lg.info ("")
			output = stringFunctions.tabs(3) + "" + type
			message = lg.infoMessage (output, message)
			if type == "nearLine":
				fullPathDirectory =  SANpath + localcssPath
				output = stringFunctions.tabs(3) + "fullPathDirectory:  " + fullPathDirectory
				message = lg.infoMessage (output, message)
				
				resultDirectoryDelete = comWrap.comWrapDelete (fullPathDirectory)
				if resultDirectoryDelete == 1:
					output = stringFunctions.tabs(3) + "Problem deleting directory:  " + fullPathLocalSplitPath
					message = lg.warnMessage (output, message)
										
				lg.info ("")
				
			if type == "archiveGraphix":
				fullPathDirectory =  localcssPath
				output = stringFunctions.tabs(3) + "fullPathDirectory:  " + fullPathDirectory
				message = lg.infoMessage (output, message)
	retObj.setRetVal(0)
	retObj.setResult(message)
	return retObj
			
def checkCSS(lg, dictVar, pushList, type, remoteHost, user, stage ):
	retObj = funcReturn.funcReturn('checkCSS')
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################	
	dictVar['prefix']="checkCSS"
 	onTapeList = []
	onCacheList = []
	count = 0
	listLength=len(pushList) 
	lg.info ("")
	message = "\tFUNCTION checkCSS"
	
	output = stringFunctions.tabs(1) + "Determine if CSS received files"
	message = lg.infoMessage (output, message)
	
	output = stringFunctions.tabs(1) + "pushList length: " + str(listLength)
	message = lg.infoMessage (output, message)
	
	hostName=socket.gethostname()
	message = ""

	notOnCache = 0
	notOnTape = 0 
	onTape = 0
	onCache = 0
 	for item in pushList:	
		localcssPath = ""
		archiveName = ""
		fullPathLocalSplitPath = ""
		cssBackupArchive = ""
		count = count + 1
		output = stringFunctions.tabs(1) + "count: " + str(count) + " of " + str(listLength)
		message = lg.infoMessage (output, message)
		#lg.info ("\titem:  "+ str(item))
		
		localcssPath = item[0]
		archiveName = item[1]
		fullPathLocalSplitPath = item[2]
		cssBackupArchive = item[3]
		
		if (type == "archive"):
			relDir = "Media/Repository/"
			archiveDirTempList = archiveName.split('.')
			archiveNameMod = archiveDirTempList[0]
			localcssPath = relDir + archiveNameMod.rstrip()
		output = stringFunctions.tabs(2) + "localcssPath:  "+ localcssPath
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "archiveName:  "+ archiveName
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "fullPathLocalSplitPath:  "+ fullPathLocalSplitPath
		message = lg.infoMessage (output, message)
		
		output = stringFunctions.tabs(2) + "tcssBackupArchive:  "+ cssBackupArchive
		message = lg.infoMessage (output, message)
				
		#confirm CSS archive has been move from cache to tape
		#$i/$cssPartPath`
		archiveList = []
		archiveList = fileFunctions.listFromFile(archiveFile)
		totalSizePushed = 0

		for a in archiveList:
			remotePathDst = a.rstrip() + "/" + localcssPath + "/" + archiveName.rstrip()
			
			output = stringFunctions.tabs(2) + "remoteHost:  " + remoteHost
			message = lg.infoMessage (output, message)
		
			output = stringFunctions.tabs(2) + "user:  " + user
			message = lg.infoMessage (output, message)
		
			output = stringFunctions.tabs(2) + "remotePathDst:  " + remotePathDst
			message = lg.infoMessage (output, message)
		
			output = stringFunctions.tabs(2) + "stage:  " + stage
			message = lg.infoMessage (output, message)
		
			retObj=masStoreFunc.checkTape(remoteHost, user, remotePathDst, outputparamikoLogFile, stage)
			retVal=retObj.getRetVal()
			output = stringFunctions.tabs(2) + "retVal:  " + str(retVal)
			message = lg.infoMessage (output, message)
					
			comment = retObj.getComment()
			output = stringFunctions.tabs(2) + "comment:  " + str(comment)
			message = lg.infoMessage (output, message)
					
			if retVal == 1:
				onCache = onCache + 1
				notOnTape = notOnTape + 1
			else:
				command = comment
				output = stringFunctions.tabs(2) + "command:  " + str(command)
				message = lg.infoMessage (output, message)
			
				output = stringFunctions.tabs(2) + "retVal:  " + str(retVal)
				message = lg.infoMessage (output, message)
					
				stdOut = retObj.getStdout()
				output = stringFunctions.tabs(2) + "stdOut:  " + str(stdOut)
				message = lg.infoMessage (output, message)
				
				charResult =  stdOut[0]
				output = stringFunctions.tabs(3) + "charResult:  "+ charResult
				message = lg.infoMessage (output, message)
				
				if ( charResult == 'M' or charResult == 'm' ):
					onTape = onTape + 1 
				else:
					notOnTape = notOnTape + 1 
			output = stringFunctions.tabs(3) + "notOnCache:  " + str(notOnCache)
			message = lg.infoMessage (output, message)
			
			output = stringFunctions.tabs(3) + "onCache:  " + str(onCache)
			message = lg.infoMessage (output, message)
				
			output = stringFunctions.tabs(3) + "notOnTape:  " + str(notOnTape)
			message = lg.infoMessage (output, message)
			
			output = stringFunctions.tabs(3) + "onTape:  " + str(onTape)
			message = lg.infoMessage (output, message)
				
			#check to make sure that we received information from all archive repositories	
			if ( onCache > 0 ):
				fileFunctions.listToFile( onCacheList, onCacheFile )
				messagNew =  "\t\t\tWARNING:   " + str(a.rstrip()) + " -  still on cached: " + localcssPath 
				message = message + messagNew + "\n"
				lg.warn (messagNew)
				retObj.setError(message)
			#check to make sure that we received information from all archive repositories has be transferred from cache to tape	
			elif ( notOnTape > 0 ):
				fileFunctions.listToFile( onCacheList, onCacheFile )
				messagNew =  "\t\t\tWARNING:   " + str(a.rstrip()) + " -  not on tape: " + localcssPath 
				message = message + messagNew + "\n"
				lg.warn (messagNew)
				retObj.setError(message)
				
		#M or m means the archive is on CSS and has been moved to tape	
		if ( notOnTape == 0 ):
			onTapeList.append (localcssPath + "," + archiveName  + "," + fullPathLocalSplitPath )
		#archive is still on the cache
		else:
			onCacheList.append (localcssPath + "," + archiveName + "," + fullPathLocalSplitPath + "," + cssBackupArchive)
	
	retDict = {'onTapeList':onTapeList ,'onCacheList':onCacheList, 'message':message}		
	retObj.setResult(retDict)	
	retObj.setRetVal(0)
	return retObj
				
def createListArchives(lg, dictVar, type, stage ):
	retObj = funcReturn.funcReturn('createListArchives')
	message = stringFunctions.tabs(1) + "FUNCTION createListArchives \n"
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################	
	dictVar['prefix']="createListArchives"
	#find list in files to archive
	searchList = []
	searchDirectories = scriptDir + searchDirectories
	if stage == "production":
		searchList = listFunctions.listFromFile(searchDirectories)
	elif stage == "other":
		searchList = listFunctions.listFromFile(searchDirectories)
	else:
		searchList = listFunctions.listFromFile(searchDirectories)
	os.chdir(scriptDir)
	cur = os.getcwd()
	output = stringFunctions.tabs(2) + "current directory:  " + cur
	message = lg.infoMessage (output, message)	
	
	archiveList = []
	output = stringFunctions.tabs(2) + "archiveFile:  " + archiveFile
	message = lg.infoMessage (output, message)	
		
	archiveList = listFunctions.listFromFile(archiveFile)
	
	noAchives = len(archiveList)
	output = stringFunctions.tabs(2) + "Get list of files archived"
	message = lg.infoMessage (output, message)
	
	output = stringFunctions.tabs(2) + "number of archives:  "+ str(noAchives)
	message = lg.infoMessage (output, message)
	lg.info (" ")
	
	pushList = []
	if os.path.exists(pushListFile):
		pushList = fileFunctions.listFromFile(pushListFile)
	listLength=len(pushList) 
	output = stringFunctions.tabs(2) + "pushList length: " + str(listLength)
	message = lg.infoMessage (output, message)

	output = stringFunctions.tabs(2) + "type:  " + type
	message = lg.infoMessage (output, message)
	
	pushList = []
	splitTarDirList = []
	#create a list of tar splits based on the directories within splitTarDirList
	splitTarDirList = listFunctions.listFromFile(splitTarDirListFile)
	for s in splitTarDirList:
		proccessed = s.rstrip()
		ooutput = stringFunctions.tabs(2) + "proccessed:  " + proccessed
		message = lg.infoMessage (output, message)
		dirContentsSplit = glob.glob(proccessed +  "/*" )
		baseDir = os.path.basename(proccessed)
		for d in dirContentsSplit:
			output = stringFunctions.tabs(3) + "d:  " + d
			message = lg.infoMessage (output, message)
			#get file name
			baseSplitTar = os.path.basename(d)
			
			#split file name on the period
			bits = baseSplitTar.split(".")
			output = stringFunctions.tabs(4) + "bits[0]:  " + bits[0]
			message = lg.infoMessage (output, message)
			if type == "nearLine":
				#get directory name
				baseDir = os.path.basename(proccessed)
				#file to be placed nearline
				relDir = baseDir + "/"+ bits[0]
		
			if type == "archiveGraphix":
				dirAlpha = bits[0][0]
				#file to be placed nearline
				relDir = dirAlpha + "/"+ bits[0]
				
			if type == "archive":
				#going to places files into repository still on SAN
				relDir = CSSaddedPath + bits[0]
			
# 			relDir = baseDir + "/"+ bits[0]
# 			lg.info ("\t\t\trelDir:  " + relDir)
# 			lg.info ("\t\t\tbaseSplitTar:  " + baseSplitTar)
# 			lg.info ("\t\t\tcssArchive:  " + cssArchive)
		 	pushList.append([relDir, baseSplitTar, d, cssArchive])

	retDict = {'pushList':pushList, 'message':message}
	retObj.setResult(retDict)	
	retObj.setRetVal(0)
	return retObj