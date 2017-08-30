#!/usr/bin/python
try:
	import os, glob, sys
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
except ImportError:
	print "missing modules for tarSplit.py"
	sys.exit(1)

def tarSplit (lg, amount, unit, mailList, stage, baseAssign, variableAssign):
	lg.setPrefix ("Tarsplit")
	lg.info ("tarsplit function")	
	
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
	############## variable assignments - end #####################
		
	############################# main - begin ###########################
	if os.path.exists(resultsFindings):
		os.unlink(resultsFindings)
	if os.path.exists(splitList):
		os.unlink(splitList)
		
	#find list in files to archive
	searchList = []
	if stage == "production":
		searchList = listFunctions.listFromFile(searchDirectories)
	elif stage == "other":
		searchList = listFunctions.listFromFile(searchDirectories)
	else:
		searchList = listFunctions.listFromFile(searchDirectories)
	
	#get iterate through list of directories to process
	dirContents = []
	for d in searchList:	
		lg.info ("\tdirectory:  "+ d.rstrip())
		#split on whitespace
		term =d.split()
		
		#get contents of directory
		dirContentsTemp = glob.glob(term[0] + "/*" )
		
		#searches broken down into search with or without exclusions 
		countTerms = len(term)
		
		for t in dirContentsTemp:
			if t.find("nearLinels") == -1 :
				lg.info ("\t\titem:  " + t )
				#if count terms is one add entire directory
				if countTerms == 1:
					dirContents.append(t)
				#if count term is not one add entire directory except for second term
				else:
					if d.find(term[1]) == -1:
						dirContents.append(t)
				
		#remove wildcard entries from list of paths	
		listFunctions.removeValuesList (dirContents, term[0] + "/*" )
	
	
	#set amount for split
	splitAmount = str(fileFunctions.convertToBytes ( 100, "GB" ))
	
	#set amount to send
	sendAmount =  str(fileFunctions.convertToBytes ( amount, unit ))
	
	#rename directories, removing undesirable characters
	splitTarList = []
	archiveTotal = 0
	totalDuration = 0
	for d in dirContents:	
		dict=archiveFunc.archivePrep (lg, d, tempSplit)
		result = dict['retVal']
		if result == 0:
			path=dict['path']
			baseOrig=dict['baseOrig']
			dirUpFull=dict['dirUpFull']
			dirUp=dict['dirUp']
			tempSplitFull=dict['tempSplitFull']
			comment=dict['comment']
			command=dict['command']

			lg.info ("\t\t\t")
			lg.info ("\t\t\td:             " + d )
			lg.info ("\t\t\tpath:          " + path )
			lg.info ("\t\t\tbaseOrig:      " + baseOrig )
			lg.info ("\t\t\tdirUpFull:     " + dirUpFull )
			lg.info ("\t\t\tdirUp:         " + dirUp )
			lg.info ("\t\t\ttempSplitFull: " + tempSplitFull )
			lg.info ("\t\t\tcomment:       " + comment )
			lg.info ("\t\t\tcommand:       " + command )
		else:
			mailList['subject'] = mailList['message'] = message = "unable to make directory: " +  tempSplitFull 
			simpleMail.shortMessage (mailList)
			lg.abort ( "\t\t\tunable to make directory: " +  tempSplitFull )
			sys.exit(1)
	
		################################## prepare file and dir - begin ##################################		
		#remove offensive char
		base=fileFunctions.removeBadChar(baseOrig)
		lg.info ("\t\t\t")
		lg.info ("\t\t\tprepare file and dir start")
		lg.info ("\t\t\tbase remove char:  " + base )
		
		base=fileFunctions.convertNameToCamel (base, "_")
		lg.info ("\t\t\tbase upper char:  " + base )
		
		if base != baseOrig:
			newFullPath = dirUpFull + "/" + base
			lg.info ("\t\t\td:            " + d )
			lg.info ("\t\t\tnewFullPath:  " + newFullPath)		
			try:
				os.renames (d, newFullPath)
			except Exception as e:
				dict['error'] = "rename error:  " + d
				try:
					shutil.move(d, newFullPath)
				except Exception as e:
					dict['error'] = dict['error'] + "\n shutil move error:  " + d
					mailList['subject'] = mailList['message'] = message = "unable to rename directory: " +  d 
					simpleMail.shortMessage (mailList)
					lg.abort ( "       unable to make directory: " +  d )
					sys.exit(1)
			lg.info ("        renamed file")
		else:
			newFullPath=d
		
		lg.info ("\t\t\tnewFullPath:        " + newFullPath )
		#get partial path  i.e.  readyToArchive/blahblah
		replaceString = ""
		cssPath = newFullPath.replace(SANpath, replaceString)
		lg.info ("\t\t\tcssPath:        " + cssPath )
	
		#nouchg files
		result=fileFunctions.nouchg(newFullPath)
		if result != 0:
			mailList['subject'] = mailList['message'] = message = "archive - unable to unlock all files:  " +  baseOrig 
			simpleMail.shortMessage (mailList)
			lg.abort ( "\t\t\tunable to change flags of files:  " +  baseOrig)
			sys.exit(1)

		directory.setPosixRec ( newFullPath, "ladmin", 0770 ) 
		lg.info ("\t\tprepare file and dir end")
		lg.info ("")
		################################## prepare file and dir - end ##################################	
		
		################################## split - begin ##################################			
		lg.info ("\t\t\tsplit began")
		archiveNameFull = tempTar + base + ".tar"
		splitFull = tempSplit + dirUp + "/" + base + ".tar.part-"
		lg.info ("\t\t\tarchiveNameFull: " + archiveNameFull)
		lg.info ("\t\t\tsplitFull: "       + splitFull)
		lg.info ("\t\t\tnewFullPath: "     + newFullPath)
		lg.info ("\t\t\tsplitAmount: "     + splitAmount)
		lg.info ("")
		#remove old files if they exist
		directory.purge(tempSplitFull, splitFull)
			
		sizeOfDir = directory.dirSize(newFullPath)
		humanSizeOfDir = fileSize.file_Size(sizeOfDir)	
		
		lg.info ("        size of Directory:  " + str(humanSizeOfDir))
		#estimate of tar
		archiveTotal += sizeOfDir
		
		if sendAmount > archiveTotal:
		    paraList = [ archiveNameFull, newFullPath, splitFull, splitAmount ]	
		    resultDict = fileFunctions.makeArchiveSplitReturn (paraList)
		    durationSeconds=resultDict['seconds']
		    durationMinutes=durationSeconds / 60
		    totalDuration += durationMinutes
		    lg.info ("\t\t\t%d seconds" % (durationSeconds))
		    lg.info ("\t\t\t%d minutes" % (durationMinutes))
		    sizeArchive=resultDict['size']
		    retObjSize=fileSize.file_Size( sizeArchive )
		    gb=retObjSize.getGB()
		    lg.info ("\t\t\tsize of archive bytes:  " + str(sizeArchive))
		    lg.info ("\t\t\tsize of archive :  " + str(gb) + " GB")
		    if durationMinutes > 0:
		    	gbPerMin = gb / durationMinutes
		    	lg.info ("\t\t\tgb per min:  " + str(gbPerMin))
		    #create more accurate accounting of tar size
		    archiveTotal -= sizeOfDir
		    archiveTotal += sizeArchive
		    retObjSize=fileSize.file_Size( archiveTotal )
		    gb=retObjSize.getGB()
		    
		    lg.info ("    ")
		    lg.info ("\t\t\tTotal size of archive:  " + str(gb))
			
		    #create a list of split items, sanPath, cssPath
		    #will replace this code and place it in pushCSS
		    dirContentsSplit = glob.glob(splitFull + "*" )
		    for s in dirContentsSplit:
				lg.info ("    ")
				lg.info ("\t\t\ts:  " + s)
				backupTerm=[]
				baseSplit = os.path.basename(s)
				lg.info ("\t\t\tbaseSplit:  " + baseSplit)
				backupTerm=cssPath.split('/')
				backupCheck=backupTerm[0].strip()
				lg.info ("\t\t\tbackupCheck:  _" + backupCheck + "_")
				lg.info ("\t\t\tbackup:  _" + backup + "_")
				if backupCheck == backup:
					cssBackupArchive=cssBackup
					lg.info ("\t\t\tcssBackup  ")
					lg.info ("\t\t\tcssBackupArchive:  " + cssBackupArchive)
					noDate=dirWithoutDate(base)
					lg.info ("\t\t\tnoDate:  " + noDate)
					dirN=os.path.dirname(cssPath)
					cssPath=dirN+ "/" + noDate
					lg.info ("\t\t\tdirN:  " + dirN)
					lg.info ("\t\t\tcssPath:  " + cssPath)
					splitTarList.append(cssPath + " " + base + " " + baseSplit + " " +  newFullPath + " " + cssBackupArchive)
				else:
					cssBackupArchive=cssArchive
					lg.info ("\t\t\tcssArchive  ")
					lg.info ("\t\t\tcssBackupArchive:  " + cssBackupArchive)
					splitTarList.append(cssPath + " " + base + " " + baseSplit + " " +  newFullPath + " " + cssBackupArchive)
	
	if totalDuration > 0:
		gb = humanTotal.getGB()
		gbPerMin = gb / totalDuration
		lg.info ("\t\t\tTotal gb per min:  " + str(gbPerMin))
		    			
	#create a file of split items, sanPath, cssPath
	fileFunctions.listToFile( splitTarList, splitList)	

	directory.setPosixRec ( tempSplit, "ladmin", 0770 ) 
	lg.info ("\t\t\tsplit end")
	################################## split - end ##################################			

	############################# main - end ###########################
