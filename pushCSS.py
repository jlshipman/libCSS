#!/usr/bin/python
try:
	import socket, os, sys, glob
	sys.path.append('lib')
	sys.path.append('libCSS')
	import listFunctions
	import masStoreFunc
	import comWrap
	import directory
	import fileSize
	import fileFunctions
	import simpleMail
	import dictFunc
	
except ImportError:
	print "missing modules for pushCSS.py"
	sys.exit(1)

def pushCSS (lg, mailList, baseAssign, variableAssign, type):
	lg.setPrefix ("pushCSS")
	lg.info ("pushCSS function")	
	############## variable assignments - begin #####################
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
	hostName=socket.gethostname()
	############## variable assignments - end #####################

	############################# main - begin ###########################
	if os.path.exists(fullPathpushListFile):
		os.unlink(fullPathpushListFile)
	if os.path.exists(tempMasmkdirError):
		os.unlink(tempMasmkdirError)
	if os.path.exists(tempMasPutError):
		os.unlink(tempMasPutError)

	os.putenv("MSSUSER", "jshipman")
	os.putenv("MSSHOST", "css-10g")
	pushList = []
	#get info from file
	tarSplitList = []
	splitTarDirList = []
	#create a list of tar splits based on the directories within splitTarDirList
	splitTarDirList = listFunctions.listFromFile(splitTarDirListFile)
	for s in splitTarDirList:
		proccessedS = s.rstrip()
		#lg.info ("      proccessedS:  " + proccessedS)
		dirContentsSplit = glob.glob(proccessedS +  "/*" )
		baseDir = os.path.basename(proccessedS)
		for d in dirContentsSplit:
			#lg.info ("      d:  " + d)
			baseSplitTar = os.path.basename(d)
			bits = baseSplitTar.split(".")
			lg.info ("\t\t\tbits[0]:  " + bits[0])
			if type == "archive":
				relDir = CSSaddedPath + bits[0]
			else:
				relDir = baseDir + "/"+ bits[0]
			lg.info ("\t\t\trelDir:  " + relDir)
			lg.info ("\t\t\tbaseSplitTar:  " + baseSplitTar)
			lg.info ("\t\t\td:  " + d)
			lg.info ("\t\t\tcssArchive:  " + cssArchive)
		 	tarSplitList.append([relDir, baseSplitTar, d, cssArchive])
	
	#order tarSplitList by d
	tarSplitList.sort(key = lambda row: row[2])
	for d in tarSplitList:
		lg.info ("\t\t\td:  " + str(d[2]))
	archiveList = []
	archiveList = listFunctions.listFromFile(archiveFile)
	totalSizePushed = 0
	for a in archiveList:
		archive=a.rstrip()
		totalSizeArchive = 0
		splitListLen = len(tarSplitList)
		count = 0
		for t in tarSplitList:
			count = count + 1
			
			relativeCSSPathDir = t[0]
			splitFileName = t[1]
			localFullPath = t[2]
			cssBackupArchive = t[3]
		
			os.putenv("MASCD", cssBackupArchive)
				
			lg.info ("  ")
			lg.info ("\t" + archive + ":  " + str(count) + " of " + str(splitListLen))
			lg.info ("\t\t\trelativeCSSPathDir:  " + relativeCSSPathDir)
 			lg.info ("\t\t\tsplitFileName:  " + splitFileName)
 			lg.info ("\t\t\tcssBackupArchive  " + cssBackupArchive)
 			lg.info ("\t\t\tlocalFullPath  " + localFullPath)			
 			lg.info ("\t\t\thostName:  " + hostName)
 			
 			
			cssDir=archive + "/" + hostName + "/" + relativeCSSPathDir
			cssPath=cssDir + "/" + splitFileName
			
			lg.info ("\t\t\tcssDir  " + cssDir)			
 			lg.info ("\t\t\tcssPath:  " + cssPath)

			curDir=os.getcwd()
 			fullPathTempMasmkdirError = scriptDir + tempMasmkdirError
			if os.path.exists(fullPathTempMasmkdirError):
				os.unlink(fullPathTempMasmkdirError)			
			resultDict=masStoreFunc.masMkdir(cssDir, fullPathTempMasmkdirError)
			result=resultDict['retVal']
			if result != 0:
				command=resultDict['command']
				lg.abort ( "      command:" + command )
				mailList['subject'] = "archive " + cssDir + " was not created" 
				message = "archive " + cssDir + " was not created/n" 
				message = message + resultDict['error'] + "/n" 
				message = message + "      command:" + command 
				mailList['message'] = message
				simpleMail.shortMessage (mailList)
				lg.abort ( "      " + cssDir + " was not created" )
				sys.exit(1)
 			
 			##########################archivefile -begin##########################
 			curDir=os.getcwd()
 			newDir = os.path.dirname(localFullPath)
			os.chdir(newDir)
 			fullPathTempMasPutError= scriptDir  +  tempMasPutError
			if os.path.exists(fullPathTempMasPutError):
				os.unlink(fullPathTempMasPutError)

 			lg.info ("\t\t\tpushing archive file: "  + splitFileName)
 			lg.info ("\t\t\t\tfullPathTempMasmkdirError:  " + fullPathTempMasmkdirError)
 			lg.info ("\t\t\t\tcssDir:  " + cssDir)
 			lg.info ("\t\t\t\tcssPath:  " + cssPath)
 			lg.info ("\t\t\t\tfullPathTempMasPutError:  " + fullPathTempMasPutError)
 			lg.info ("\t\t\t\tlocalFullPath:  " + localFullPath)

 			#new code
 			resultDict=masStoreFunc.masPutDelay2 (splitFileName, cssPath,  fullPathTempMasPutError)
			command = resultDict[ 'command']
			lg.info ("\t\t\t\tcommand:  " + command )
			result=resultDict['retVal']
 			if result != 0:
				function = resultDict[ 'function']
				lg.info ("\t\tfunction:  " + function )
				command = resultDict[ 'command']
				lg.info ("\t\tcommand:  " + command )
				error = resultDict[ 'error']
				lg.info ("\t\terror:  " + error )

				function2 = resultDict[ 'function2']
				lg.info ("\t\tfunction2:  " + function2 )
				command2 = resultDict[ 'function2Command']
				lg.info ("\t\tcommand2:  " + command2 )

				mailList['subject'] = "archive  " + splitFileName + " was not pushed"
				message = "      function:  " + function + "\n"
				message = message + "      command:  " + command + "\n"
				message = message + "      error:  " + error + "\n"
				message = message + "      function2:  " + function2 + "\n"
				message = message + "      command2:  " + command2 + "\n"
				mailList['message'] = message
				simpleMail.shortMessage (mailList)
				lg.abort ( "\t\t" + splitFileName + " was not pushed" )
				os.chdir(curDir)
				sys.exit(1)
				
			os.chdir(curDir)	
			durationSeconds=resultDict['runTotalSeconds']
			durationMinutes=durationSeconds / 60
			lg.info ("\t\t\t%d seconds" % (durationSeconds))
			lg.info ("\t\t\t%d minutes" % (durationMinutes))
			sizeArchive=os.path.getsize(localFullPath)
			lg.info ("\t\t\tsize of the archive in bytes:  %d" % (sizeArchive))  			
			retObjSize=fileSize.file_Size( amount )
			gb=retObjSize.getGB()
 			lg.info ("\t\t\tsize of archive :  " + str(gb) + " GB")
 			
 			totalSizeArchive += sizeArchive
 			retObjSize=fileSize.file_Size( totalSizeArchive )
 			gb=retObjSize.getGB() 						
 			lg.info ("\t\t\ttotal size of archive bytes:  " + str(totalSizeArchive))
 			lg.info ("\t\t\ttotal size of archive :  " + str(gb2) + " GB")
 			
 			totalSizePushed += sizeArchive
 			retObjSize=fileSize.file_Size( totalSizePushed )
 			gb=retObjSize.getGB() 						
 			lg.info ("\t\t\ttotal size of data pushed bytes:  " + str(totalSizePushed))
 			lg.info ("\t\t\ttotal size of data pushed :  " + str(gb) + " GB")
 			if durationMinutes > 0:
				gbPerMin = gb / durationMinutes
				gbPerHr = gbPerMin * 60
				lg.info ("\t\t\tgb per min:  " + str(gbPerMin))
				lg.info ("\t\t\tgb per hr:  " + str(gbPerHr))
			
			cssTarSplitFile=cssDir + "/" +  splitFileName
			fileSizeBytes = os.path.getsize(localFullPath)
		
			cssFileSize = masStoreFunc.masCSSfileSize(cssTarSplitFile)
			lg.info ( "\t\t\tcssFileSize:  " + str(cssFileSize) )
			lg.info ( "\t\t\tlocalFileSize:  " + str(fileSizeBytes) )
			lg.info ( " " )
			if int(cssFileSize) != int(fileSizeBytes):
				listToFile( pushList, fullPathpushListFile )
				mailList['subject'] = mailList['message'] = message = "archive " + splitFileName + " CSS file not same size as local copy" 
				simpleMail.shortMessage (mailList)
				lg.abort ( "\t\t" + splitFileName + " CSS file not same size as local copy")
				sys.exit(1)
			##########################archivefile -end##########################
			
			##########################checksum file of archive -begin##########################	
			checkSumFile = splitFileName + ".ck"
			lg.info ("\t\tpushing checksum file: " + checkSumFile)
			curDir=os.getcwd()
			fullPathTempCKDir = scriptDir + tempCk
			fullPathTempCK=fullPathTempCKDir + checkSumFile
			lg.info ("\t\t\tfullPathTempCKDir: " + fullPathTempCKDir)
 			os.chdir(fullPathTempCKDir)
 			fullPathTempMasPutError= scriptDir +  tempMasPutError
 			if os.path.exists(fullPathTempMasPutError):
 				os.unlink(fullPathTempMasPutError)
			cssPath=cssDir  + "/" + splitFileName + ".ck"
			lg.info ("\t\t\ttempCkcheckSumFile: " + checkSumFile)
			lg.info ("\t\t\tcssDir:  " + cssDir)
			lg.info ("\t\t\tcssPath:  " + cssPath)
			lg.info ("\t\t\tfullPathTempMasPutError:  " + fullPathTempMasPutError)
			#create checksum in second parameter based on file (first parameter)
			result=fileFunctions.checkSum2(localFullPath, checkSumFile)
			retVal = result['retVal']
			if retVal != 0:
				listToFile( pushList, fullPathpushListFile )
				mailList['subject'] = mailList['message'] = message = "archive " + checkSumFile + " was not created" 
				simpleMail.shortMessage (mailList)
				error = result['error']
				lg.abort ( "\t\terror:  " + error )
				lg.abort ( "\t\t" + checkSumFile + " was not created" )
				sys.exit(1)
			resultDict=masStoreFunc.masPutDelay2 (checkSumFile, cssPath,  fullPathTempMasPutError, 3)
			result=resultDict['retVal']
			if result != 0:
				listToFile( pushList, fullPathpushListFile )
				function = resultDict[ 'function']
				lg.info ("\t\tfunction:  " + function )
				command = resultDict[ 'command']
				lg.info ("\t\tcommand:  " + command )
				error = resultDict[ 'error']
				lg.info ("\t\terror:  " + error )

				function2 = resultDict[ 'function2']
				lg.info ("\t\tfunction2:  " + function2 )
				command2 = resultDict[ 'function2Command']
				lg.info ("\t\tcommand2:  " + command2 )

				mailList['subject'] = "archive  " + checkSumFile + " was not pushed"
				message = "      function:  " + function + "\n"
				message = message + "      command:  " + command + "\n"
				message = message + "      error:  " + error + "\n"
				message = message + "      function2:  " + function2 + "\n"
				message = message + "      command2:  " + command2 + "\n"
				mailList['message'] = message
				simpleMail.shortMessage (mailList)
				lg.abort ( "\t\t" + checkSumFile + " was not pushed" )
				sys.exit(1)
			else:
				if fileFunctions.fileExist (checkSumFile):
					lg.info ("\t\tcheckSumFile is being deleted:  " + checkSumFile )
					os.unlink(checkSumFile)	
			##########################checksum file of archive -end##########################		
			pushList.append(cssPath + " " + relativeCSSPathDir + " " + splitFileName + " " + cssBackupArchive)

	#create a file with css Path of archive, archive directory on local machine, split file on local machine
	fileFunctions.listToFile( pushList, fullPathpushListFile )
####################
