#!/usr/bin/python
try:
	import os, glob, sys, datetime
	sys.path.append('lib')
	from log import *
	from timeFunc import *
	from directory import *
	from listFunctions import *
	from fileFunctions import *
	from simpleMail import *
	from dictFunc import *
except ImportError:
	print "missing modules for versions.py"
	sys.exit(1)

#input
#log
#
#output
#create a new run list with updated times  -- versionDirectories.txt
#
#reads in file of searchable directories. 
#copies items to selected directory

def versions (lg, mailList, dictVar, type, stage, remoteHost, user):
	retObj = funcReturn.funcReturn('versions')
	############## variable assignments - end #####################
	lg.setPrefix ("Version")
	lg.info ("versions function")	
	
	############## variable assignments - begin #####################
	for (n, v) in dictVar.items():
		exec('%s=%s' % (n, repr(v)))	
	############## variable assignments - end #####################

	nowTime=datetime.now().strftime('%Y%m%d%H%M')
	nowDate=datetime.now().strftime('%Y_%m_%d')
	############## variable assignments - end #####################
		
	############################# main - begin ###########################
	
	##### get info from file - begin #####
	searchList = []
	newList = []
	dirContents = []

	if stage == "production":
		versionDir=versionDirectories
	else:
		versionDir=versionDirectoriesDev
		
	f = open(versionDir)
	lines = f.readlines()
	
	for line in lines:
		lg.info ("  line:  " + line )
		searchList.append(line)
	f.close()
	#####get info from file - end #####
	
	##### delete current contents residing in destination - begin #####
	lg.info ("  deleting:  " + basePath )
	deleteFileOrFolder (basePath)
	lg.info ("  creating directories for transferred info")
	##### delete current contents residing in destination - end #####

	##### delete current contents residing in destination - begin #####
	
	##### make directories based on given file contencts - begin #####
	for l in searchList:	
		term = l.split()
		dir = term[0]
		lg.info ("    "+ dir)
		makeDirectory (dir)
	##### make directories based on given file contencts - end #####

	lg.info ("  setting privilege and ownership of created files:  "+ basePath)
	setPosixRec ( basePath, "ladmin", 0700 ) 

	##### create file of given searches - begin #####	
	lg.info ("  creating result file of searched directories")
	#l is storagePath searchPath dateSearched exclusionTerm
	#currently storagePath is not used
	#get list of items to be copied
	
	for l in searchList:
		lg.info ("  l:  " + l )
		term = l.split()		
		countTerms = len(term)
		lg.info ("  countTerms:  " + str(countTerms) )		
		#searches broken down into search with or without exclusions 
		dirContentsTemp = glob.glob(term[1] + "/*" )
		for d in dirContentsTemp:
			if countTerms == 3:
				newList.append(term[0] + " " + term[1] + " " + term[2] )								
			else:
				newList.append(term[0] + " " + term[1] )
				dirContents.append(d)
							
			#remove wildcard entries from list of paths	
			removeValuesList (dirContents, term[1] + "/*" )
	##### create file of given searches - end #####	
	
	lg.info ("  comparing search results against last run of script")		
	#copy items based on last time the script run
	#at this level the contents should be directories only
	if fileExist(versionRunDate):
		f = open(versionRunDate)
		lastRun = f.readline().strip()
		f.close()
	else:
		lastRun = "200101021212"

	##### compare dates conditional for copy - begin #####			
	for d in dirContents:
		fromPath =  d
		lg.info ("    d:  " + d)
		if os.path.exists(fromPath):
			if os.path.isdir(fromPath):
				t = os.path.getmtime(fromPath)
				fileModTime=datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')
				lastRunTime = stringToTime(lastRun)
				if time1BiggerThantime2 ( fileModTime, lastRunTime ):
					replaceString = "/Volumes/vodeSAN/Media/"
					dirName = os.path.basename(fromPath) 
					lg.info ("      dirName:  " + dirName)
					toPath = fromPath.replace(replaceString, basePath) + "_" + nowDate
					lg.info ("      fromPath:  " + fromPath)
					lg.info ("      toPath:    " + toPath)
					copyRecursiveDate(fromPath, toPath, lastRun)
			else:
				lg.warn ( "      " + fromPath + " is not a directory")	
		else:
			lg.warn (  "      " + fromPath + " does not exist")	
	##### compare dates conditional for copy - end #####			

	
	lg.info ("   setting privilege and ownership of copied files:  ")			
	setPosixRec ( basePath, "ladmin", 0700 )  
	if fileExist(versionRunDate):	
		fileDelete(versionRunDate)
	f = open(versionRunDate, "wb")
	f.write(nowTime)
	f.close()
	
	retObj.setRetVal(0)
	return retObj
