#!/usr/bin/python
#try:
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
import funcReturn	
import remoteFunc
import datetime
import stringFunctions
import timeFunc

#except ImportError:
	#print "missing modules for pushCSS.py"
#	sys.exit(1)

def pushCSS2 (lg, mailList, dictVar, type, stage, remoteHost, user):
	retObj = funcReturn.funcReturn('pushCSS')
	lg.setPrefix ("pushCSS")
	now = datetime.datetime.now()
	start_time = datetime.datetime.now()
	start = now.strftime("%Y_%m_%d_%H_%M")
	subject = "FUNCTION pushCSS2    " + start
	message = subject + "\n"
	lg.info ("FUNCTION pushCSS2")
	
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################

	############################# main - begin ###########################
	if os.path.exists(fullPathpushListFile):
		os.unlink(fullPathpushListFile)
	if os.path.exists(tempMasmkdirError):
		os.unlink(tempMasmkdirError)
	if os.path.exists(tempMasPutError):
		os.unlink(tempMasPutError)

	pushList = []
	tarSplitList = []
	splitTarDirList = []
	
	retObjTarSplitList=createTarSplitList(lg, dictVar, type, stage)
	tarSplitList = retObjTarSplitList.getResult()
	
	#lastFilePushed

	#list of archive names
	#	archive1
	#	archive2
	archiveList = []
	archiveFile=scriptDir + archiveFile
	archiveList = listFunctions.listFromFile(archiveFile)
	totalSizePushed = 0
	hostName=socket.gethostname()

	lg.info ("  ")
	
	#need to implement
	#find size of list
	#find index of given value in list
	#create range to iterate thru
	#for a in archiveList[1:3]:
	countArchive = 0
	archiveLen = len(archiveList)
	for a in archiveList:
		countArchive = countArchive + 1
		lg.info ("archive:  " + str(countArchive) + " of " + str(archiveLen))
		archive=a.rstrip()
		totalSizeArchive = 0
		totalSecArchive = 0
		splitListLen = len(tarSplitList)
		count = 0
		for t in tarSplitList:
			count = count + 1
			
			relativeCSSPathDir = t[0]
			splitFileName = t[1]
			localFullPath = t[2]
			cssBackupArchive = t[3]
					
			lg.info ("\ttarSplits:  "  + str(count) + " of " + str(splitListLen))
			lg.info ("\t\tt:  " + str(t))
			lg.info ("  ")
			lg.info ("\t\tsplitFileName:  " + splitFileName)
			lg.info ("  ")
			lg.info ("\t\t\trelativeCSSPathDir:  " + relativeCSSPathDir)
 			lg.info ("\t\t\tcssBackupArchive  " + cssBackupArchive)
 			lg.info ("\t\t\tlocalFullPath  " + localFullPath)			
 			lg.info ("\t\t\thostName:  " + hostName)
 			
			#cssDir=archive + "/" + hostName + "/" + relativeCSSPathDir
			cssDir=archive + "/" + relativeCSSPathDir
			cssPath=cssDir + "/" + splitFileName
			
			lg.info ("\t\t\tcssDir  " + cssDir)			
 			lg.info ("\t\t\tcssPath:  " + cssPath)
 			
			#create directory on CSS
			retObjMkdir=remoteMkdirMail (lg, mailList, remoteHost, user, cssDir, outputparamikoLogFile, stage)
			if retObjMkdir.getRetVal() == 1:
				sys.exit(1)
 			##########################archivefile -begin##########################
 			#change to archives directory
 			curDir=os.getcwd()
 			newDir = os.path.dirname(localFullPath)
			os.chdir(newDir)
			lg.info ("")
 			lg.info ("\t\t\tpushing archive file: "  + splitFileName)
  			lg.info ("\t\t\t\tcssDir:  " + cssDir)
 			lg.info ("\t\t\t\tcssPath:  " + cssPath)
 			lg.info ("\t\t\t\tlocalFullPath:  " + localFullPath)

			#place local file in remote host directory.
			retObjPutFile=remotePutFileMail (lg, mailList, remoteHost, user, cssDir, localFullPath, outputparamikoLogFile, stage)
			if retObjPutFile.getRetVal() == 1:
				sys.exit(1)
				
			results = retObjPutFile.getResult()
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
			if totalMinArchive > 0:
				gbPerMin = gb / totalMinArchive
				gbPerHr = gbPerMin * 60
				lg.info ("\t\t\tgb per min:  " + str(gbPerMin))
				lg.info ("\t\t\tgb per hr:  " + str(gbPerHr))
			lg.info ("")	
			#change to original directory
			os.chdir(curDir)	

			##########################archivefile -end##########################
			
			##########################checksum file of archive -begin##########################	
			print "pushCSS2 - checksum file of archive"
			print "\tremoteHost:              " + remoteHost
			print "\tuser:                    " + user
			print "\tcssDir:                  " + cssDir
			print "\tlocalFullPath:           " + localFullPath
			print "\toutputparamikoLogFile:   " + outputparamikoLogFile
			print "\tstage:                   " + stage
			retOjb=remotePutCKMail(lg, mailList, remoteHost, user, cssDir, localFullPath, outputparamikoLogFile, stage)
			if retOjb.getRetVal() == 1:
				sys.exit(1)
	
			##########################checksum file of archive -end##########################		
			pushList.append(cssPath + " " + relativeCSSPathDir + " " + splitFileName + " " + cssBackupArchive)
			
			####create file with last file pushed#######
			lastFilePushed = a + "#" + relativeCSSPathDir  + "#" + splitFileName + "#" + localFullPath + "#" + cssBackupArchive
			retObjlastFile=fileFunctions.fileCreateWrite(lastFilePushedFile, lastFilePushed)
			retVal=retObjlastFile.getRetVal()
			error=retObjlastFile.getError()


	now = datetime.datetime.now()
	end = now.strftime("%Y_%m_%d_%H_%M")
	output = "pushCSS2:  end - " + end
	message = lg.infoMessage (output, message)
	end_time = datetime.datetime.now()
	timeDict = timeFunc.timeDuration2 (end_time, start_time)
	printHours = timeDict['printHours']
	printMins = timeDict['printMins']
	printSec = timeDict['seconds']
	output = "migration took " + str(printHours) + ":" + str(printMins) + " or " + str(printSec) + " seconds to run"
	message = lg.infoMessage (output, message)
	
	#create a file with css Path of archive, archive directory on local machine, split file on local machine
	fileFunctions.listToFile( pushList, fullPathpushListFile )
	retObjDeleteFile=fileFunctions.fileDirDelete(lastFilePushedFile)
	retObj.setRetVal(0)
	return retObj
	
####################

def createTarSplitList(lg, dictVar, type, stage):
	retObj = funcReturn.funcReturn('createTarSplitList')
	lg.info ("\tcreateTarSplitList")
	#create variables from list
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))
		
	splitTarDirListFile = scriptDir + splitTarDirListFile
	
	tarSplitList = []

	#create a list of tar splits based on the directories within splitTarDirList
	
	splitTarDirList = listFunctions.listFromFile(splitTarDirListFile)
	#nearLine
	#splitTarDirList contains two entries
	#    /Volumes/videoSAN/Temp/Split/nearLine/readyToArchive
	#    /Volumes/videoSAN/Temp/Split/nearLine/p2_SD
	#
	#archiveGraphix
	# /Volumes/Media/TEMP/Split/archive
	
	
	for s in splitTarDirList:
		proccessed = s.rstrip()
		lg.info ("")
		lg.info ("\t\tproccessed:  " + proccessed)
		lg.info ("")
		#gather file names of files in directory
		dirContentsSplit = glob.glob(proccessed +  "/*" )
		
		#iterate through directory contents
		for d in dirContentsSplit:
			lg.info ("\t\t\td:  " + d)
			#get file name
			baseSplitTar = os.path.basename(d)
			
			#split file name on the period
			bits = baseSplitTar.split(".")
			lg.info ("\t\t\t\tbits[0]:  " + bits[0])
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
				
				
			lg.info ("\t\t\t\trelDir:  " + relDir)
			lg.info ("\t\t\t\tbaseSplitTar:  " + baseSplitTar)
			lg.info ("\t\t\t\tcssArchive:  " + cssArchive)
		 	tarSplitList.append([relDir, baseSplitTar, d, cssArchive])
		 	
	#order tarSplitList by d
	tarSplitList.sort(key = lambda row: row[2])
	lg.info ("")
	lg.info ("\t\tsorted")
	for d in tarSplitList:
		lg.info ("\t\t\td:  " + str(d[2]))
	retObj.setResult(tarSplitList)	 	
	return retObj
	
def remoteMkdirMail (lg, mailList, remoteHost, user, cssDir, outputparamikoLogFile, stage):
	retObjMkdirCSS=remoteFunc.mkdir(remoteHost, user, cssDir, outputparamikoLogFile, stage, mode=0770)
	retVal = retObjMkdirCSS.getRetVal()
	if retVal != 0:
		Comment=retObjMkdirCSS.getComment()
		error=retObjMkdirCSS.getError()
		lg.warn ( "\t\tComment:  " + Comment )
		lg.abort ( "\t\terror:  " + error )
		mailList['subject'] = "archive directory" + cssDir + " was not created on remote host" 
		message = "archive  directory " + cssDir + " was not created on remote host \n" 
		message = message + error + "\n" 
		message = message + "\t\tComment:  " + Comment 
		mailList['message'] = message
		simpleMail.shortMessage (mailList)
		lg.abort ( "\t\tremoteMkdirMail:  " + cssDir + " directory was not created on remote host" )
	return retObjMkdirCSS
		
def remotePutFileMail (lg, mailList, remoteHost, user, remotePathDir, localPathFileSrc, outputparamikoLogFile, stage, passwd=""):
	print "remotePutFileMail"
	print "\tremoteHost:               " + remoteHost
	print "\tuser:                     " + user
	print "\tremotePathDir:            " + remotePathDir
	print "\tlocalPathFileSrc:         " + localPathFileSrc
	print "\toutputparamikoLogFile:    " + outputparamikoLogFile
	print "\tstage:                    " + stage
	base = os.path.basename(localPathFileSrc)
	remoteFilepath=remotePathDir + "/" + base
	retObjPutFile=masStoreFunc.putSSH(remoteHost, user, localPathFileSrc, remoteFilepath, outputparamikoLogFile, stage, passwd)

	retVal = retObjPutFile.getRetVal()
	if retVal == 0:
		results = retObjPutFile.getResult()
		fileProperties=results['fileProperties']
		sizeArchive = int(fileProperties['size'])
		durationSeconds = results['seconds']
		durationMinutes=durationSeconds / 60
		print "sizeArchive:  " + str(sizeArchive)
		print "durationSeconds:  " + str(durationSeconds)
		print "durationMinutes:  " + str(durationMinutes)
		
		lg.info ("\t\t\t%d seconds" % (durationSeconds))
		lg.info ("\t\t\t%d minutes" % (durationMinutes))
		lg.info ("\t\t\tsize of the archive in bytes:  %d" % (sizeArchive)) 
		retObjSize=fileSize.file_Size( sizeArchive )
		gb=retObjSize.getGB() 			
		lg.info ("\t\t\tsize of archive: bytes:  " + str(sizeArchive))
		lg.info ("\t\t\tsize of archive:  " + str(gb) + " GB")
		if durationMinutes > 0:
			gbPerMin = gb / durationMinutes
			gbPerHr = gbPerMin * 60
			lg.info ("\t\t\tgb per min:  " + str(gbPerMin))
			lg.info ("\t\t\tgb per hr:  " + str(gbPerHr))
	else:
		comments=retObjPutFile.getComment()
		error=retObjPutFile.getError()
		command=retObjPutFile.getCommand()
		lg.abort ( "\t\tcomments:  " + comments )
		base = os.path.basename(localPathFileSrc)
		mailList['subject'] = "archive file " + base + " was not created on remote host" 
		message = "archive file " + base + " was not created on remote host\n" 
		message = message + error + "\n" 
		message = message + "\t\tcomments:  " + comments 
		mailList['message'] = message
		simpleMail.shortMessage (mailList)
		lg.abort ( "\t\tremotePutFileMail:  " + base + " was not created on remote host" )
		lg.abort ( "\t\tputSSH error:  " + error )
		lg.abort ( "\t\tputSSH command:  " + command )
	return retObjPutFile
	
def remotePutCKMail (lg, mailList, remoteHost, user, remotePathDir, localPathFileSrc, outputparamikoLogFile, stage):
	print "remotePutCKMail"
	print "\tremoteHost:               " + remoteHost
	print "\tuser:                     " + user
	print "\tremotePathDir:            " + remotePathDir
	print "\tlocalPathFileSrc:         " + localPathFileSrc
	print "\toutputparamikoLogFile:    " + outputparamikoLogFile
	print "\tstage:                    " + stage

	retOjbCK=remoteFunc.putCkSum(remoteHost, user, localPathFileSrc, remotePathDir, outputparamikoLogFile, stage)
	retVal = retOjbCK.getRetVal()
	if retVal != 0:
		comment=retOjbCK.getComment()
		error=retOjbCK.getError()
		lg.abort ( "\t\tcommand:  " + comment )
		base = os.path.basename(localPathFileSrc)
		mailList['subject'] = "checksum archive file " + base + " was not created on remote host" 
		message = "checksum archive file " + base + " was not created on remote host\n" 
		message = message + error + "\n" 
		message = message + "\t\tcomment:  " + comment 
		mailList['message'] = message
		simpleMail.shortMessage (mailList)
		lg.abort ( "\t\tremotePutCKMail:  checksum archive file" + base + " was not created on remote host" )
	return retOjbCK
 			