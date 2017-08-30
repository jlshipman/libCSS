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
except ImportError:
	print "missing modules for migrate.py"
	sys.exit(1)
	
def migrate (lg, mailList, baseAssign, variableAssign, type, stage="production"):
	lg.info ("migrate function")
	lg.setPrefix ("migrate")	
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
	MSSUSER="jshipman"
	os.putenv("MSSUSER", MSSUSER)
	os.putenv("MSSHOST", "css-10g")
	
	############################# main - begin ###########################
	#get info from file
	if os.path.exists(onTapeFile):
		os.unlink(onTapeFile)
	if os.path.exists(onTapeSearchFile):
		os.unlink(onTapeSearchFile)	
		
	############################# get list of files archived - begin ###########################
	archiveList = []
	archiveList = listFunctions.listFromFile(archiveFile)
	noAchives = len(archiveList)
	lg.info ("\tGet list of files archived")
	lg.info ("\tnumber of archives:  "+ str(noAchives))
	lg.info (" ")
	
	pushList = []
	if os.path.exists(pushListFile):
		pushList = fileFunctions.listFromFile(pushListFile)
	listLength=len(pushList) 
	lg.info ("\tpushList length: " + str(listLength))
	lg.info ("\ttype:  " + type)
	pushList = []
	splitTarDirList = []
	#create a list of tar splits based on the directories within splitTarDirList
	splitTarDirList = listFunctions.listFromFile(splitTarDirListFile)
	for s in splitTarDirList:
		proccessedS = s.rstrip()
		lg.info ("\tproccessedS:  " + proccessedS)
		lg.info ("")
		dirContentsSplit = glob.glob(proccessedS +  "/*" )
		baseDir = os.path.basename(proccessedS)
		for d in dirContentsSplit:
			lg.info ("\t\td:  " + d)
			baseSplitTar = os.path.basename(d)
			bits = baseSplitTar.split(".")
			relDir = baseDir + "/"+ bits[0]
			lg.info ("\t\t\trelDir:  " + relDir)
			lg.info ("\t\t\tbaseSplitTar:  " + baseSplitTar)
			lg.info ("\t\t\tcssArchive:  " + cssArchive)
		 	pushList.append([relDir, baseSplitTar, d, cssArchive])
	############################# get list of files archived - end ###########################	
	
	############################# determine if CSS received files - begin ########################### 	
# 	cacheList = []
# 	lg.info ("  onCacheFile: " + onCacheFile)
# 	if os.path.exists(onCacheFile):
# 		cacheList = listFromFile(onCacheFile)
# 	listLength=len(cacheList) 
# 	lg.info ("  cacheList length: " + str(listLength))
# 	for item in cacheList:
# 		pushList.append (item)
# 	if os.path.exists(onCacheFile):
# 		os.unlink(onCacheFile)	
 	onTape = []
	onCache = []
	count = 0
	listLength=len(pushList) 
	lg.info ("")
	lg.info ("\tDetermine if CSS received files ")
	lg.info ("\tpushList length: " + str(listLength))
 	for item in pushList:	
		localcssPath = ""
		archiveName = ""
		fullPathLocalSplitPath = ""
		cssBackupArchive = ""
		count = count + 1
		lg.info ("\tcount: " + str(count) + " of " + str(listLength))
		#lg.info ("\titem:  "+ str(item))
		localcssPath = item[0]
		archiveName = item[1]
		fullPathLocalSplitPath = item[2]
		cssBackupArchive = item[3]
		
		os.putenv("MASCD", cssBackupArchive)
		if (type == "archive"):
			relDir = "Media/Repository/"
			archiveDirTempList = archiveName.split('.')
			archiveNameMod = archiveDirTempList[0]
			localcssPath = relDir + archiveNameMod.rstrip()
		lg.info ("\t\tlocalcssPath:  "+ localcssPath)
		lg.info ("\t\tarchiveName:  "+ archiveName)
		lg.info ("\t\tfullPathLocalSplitPath:  "+ fullPathLocalSplitPath)
		lg.info ("\t\tcssBackupArchive:  "+ cssBackupArchive)
		lg.info ("")	
		
		#confirm CSS archive has been move from cache to tape
		#$i/$cssPartPath`
		archiveList = []
		archiveList = fileFunctions.listFromFile(archiveFile)
		totalSizePushed = 0
		result = 0
		mCheck = 0 
		for a in archiveList:
			fullLocalcssPath = a.rstrip() + "/" + hostName.rstrip() + "/" + localcssPath + "/" + archiveName.rstrip()
			lg.info ("\t\t" + fullLocalcssPath)
			lg.info ("\t\t" + a.rstrip() + " - " + str(archiveName))
			dictResult=masStoreFunc.masTapeCheck3(fullLocalcssPath)
			retVal = dictResult['retVal']
			if retVal == 1:
				result = result + 1
				mCheck = mCheck + 1 
			else:
				command = dictResult['command']
				lg.info ("\t\tcommand:  "+ str(command))
				archiveResult = dictResult['result']
				#lg.info ("      archiveResult:  "+ str(archiveResult))
				if ( archiveResult == "" ):
					result = result + 1
					
				charResult =  dictResult['firstChar']
				lg.info ("\t\t\tcharResult:  "+ charResult)
				if ( charResult == 'M' or charResult == 'm' ):
					mCheck = mCheck + 0 
				else:
					mCheck = mCheck + 1 
				lg.info ("\t\t\tmCheck:  " + str(mCheck))
				lg.info (" ")
				if stage == "development":
					lg.info ("\t\t\tdevelopment:  setting mCheck to 0")
					mCheck =  0 
			#check to make sure that we received information from all archive repositories	
			if ( result > 0 ):
				fileFunctions.listToFile( onTape, onTapeFile )
				mailList['subject'] = mailList['message'] = message =  str(a.rstrip()) + " -  problem with css path: " + localcssPath
				simpleMail.shortMessage (mailList)
				lg.warn ("\t\t\t" + str(a.rstrip()) + " -  problem with css path: " + localcssPath )
				
		#M or m means the archive is on CSS and has been moved to tape	
		if ( mCheck == 0 ):
			onTape.append (localcssPath + "," + archiveName  + "," + fullPathLocalSplitPath )
		#archive is still on the cache
		else:
			onCache.append (localcssPath + "," + archiveName + "," + fullPathLocalSplitPath + "," + cssBackupArchive)
	############################# determine if CSS received files - end ########################### 
	
	############################# determine if we can move or delete files - begin ########################### 		
	fileFunctions.listToFile( onTape, onTapeFile )
	fileFunctions.listToFile( onCache, onCacheFile )	
 	#onTape = fileFunctions.listFromFile(onTapeFile)
 	#onCache = fileFunctions.listFromFile(onCacheFile)
	for items in onTape:
		(a, b, c) = items.split(",")
		localcssPath = a.rstrip()
		archiveName = b.rstrip()
		fullPathLocalSplitPath = c.rstrip()
		baseName = os.path.basename(localcssPath)
		#lg.info ("\t\titems:  " + items)
		lg.info ("\tDetermine if we can move or delete files ")
		lg.info ("\tDelete split archive:  " + fullPathLocalSplitPath)
		lg.info ("\t\tarchiveNameSplitName:  " + archiveName)
		lg.info ("\t\tlocalcssPath:  " + localcssPath)
		lg.info ("\t\tfullPathLocalSplitPath:  " + fullPathLocalSplitPath)
		lg.info ("\t\tbaseName:  " + baseName)
		#delete archive
		lg.info ("\t\tfullPathLocalSplitPath:  " + fullPathLocalSplitPath)
		resultArchiveDelete = comWrap.fileDeleteReturn(fullPathLocalSplitPath)
		if resultArchiveDelete == 1:
			lg.warn ("Problem deleting:  " + fullPathLocalSplitPath )
			
		if (type == "archive"):
			info ("")
			info ("\t\t\tarchive ")
			searchList = fileFunctions.listFromFile(searchDirectories)
			for d in searchList:	
				lg.info ("\t\t\tdirectory:  "+ d.rstrip())
				#split on whitespace
				term =d.split()
				baseName=os.path.basename(localcssPath)
				oldFullPath =  d.rstrip() + "/" + baseName
				lg.info ("\t\t\toldFullPath:  " + oldFullPath)
				if os.path.exists(oldFullPath):
					lg.info ("\t\t\told path exists")
					newFullPath =  SANpath + localcssPath
					lg.info ("\t\t\ttnewFullPath:  " + newFullPath)
					
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
					lg.info ("\t\t\told path DOES NOT exists")
		else:
			lg.info ("")
			lg.info ("\t\t\tnearline ")
			fullPathDirectory =  SANpath + localcssPath
			lg.info ("\t\t\tfullPathDirectory:  " + fullPathDirectory)
			resultDirectoryDelete = comWrap.comWrapDelete (fullPathDirectory)
			if resultDirectoryDelete == 1:
				lg.warn ("\t\t\tProblem deleting directory:  " + fullPathLocalSplitPath )
			lg.info ("")

	############################# determine if we can move or delete files - end ########################### 		
	
	hostName=socket.gethostname()
	with open(archiveFile, 'r') as f:
		archive = f.readline().rstrip()
	f.close()
	lsFileList = []
 	lsFileList = fileFunctions.listFromFile(lsFile)
	for item in lsFileList:
		term =item.rstrip().split()
		nl = term[0] + "/nearLinels.txt"	
		if os.path.exists(nl):
			os.unlink(nl)	
		cssDir=archive + "/" + hostName + "/" + term[1]
		resultDic = masStoreFunc.masDirListing ( cssDir, tempScriptDir )
		if resultDic['retVal'] == 0:
			listing = resultDic['listDirContents']
			fileFunctions.listToFile( listing, nl)
	############################# main - end ###########################
