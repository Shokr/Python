'''
	fsync
	
	Synchronizing files module, it only syncs in one direction. Handy for making backups.

	Checks on difference in modificationdate and filesize
	
	quickUse : fsync.sync(sourcepath,targetpath)

	author : Sven Fraeys
	version 1.0
'''
import os, shutil, logging

class FSyncFile:
	'''
		SyncFile
		this contains data of 1 file
	'''
	def __init__(self,source,target):
		self.source = source
		self.target = target
		
	def getLabel(self):
		return "%s>%s" % (os.path.basename(self.source), os.path.basename(self.target))
	
	def isOutdated(self):
		return is_sync_outdated(self)
	def synchronize(self):
		return synchronize(self)

def is_sync_outdated(sourcepath,targetpath):
	''' Return if two paths are synced or not.

	'''
	# check if targetpath exsists
	if not os.path.exists(targetpath):
		return True
		
	# check if modification date is different
	sourceMTime = os.path.getmtime(sourcepath)
	targetMTime = os.path.getmtime(targetpath)
	if sourceMTime > targetMTime:
		return True

	# chec if there is a different in size of the file
	sourceSize = os.path.getsize(sourcepath)
	targetSize = os.path.getsize(targetpath)
	if sourceSize != targetSize:
		return True

	# no problems, the file is in sync
	return False
	
def synchronize(syncfile,force=False):
	'''Synchornize a FSyncFile object.

	'''
	isSyncOutdated = is_sync_outdated(syncfile.source,syncfile.target)
	if isSyncOutdated or force:
		print ("syncing %s..." % str( syncfile.getLabel() ) )
		shutil.copyfile(syncfile.source, syncfile.target)

def create_SyncFile(sourcepath,targetpath):
	''' Return FSyncFile object from sourcepath and targetpath.

	'''
	if not os.path.exists(sourcepath):
		return None

	return FSyncFile(sourcepath,targetpath)
	
def sync(sourcepath,targetpath,force=False):
	''' Sync the sourcepath to targetpath.

	'''
	syncfile = create_SyncFile(sourcepath,targetpath)
	result = synchronize(syncfile,force=force)
	return result

# def synchronize_directory(target)
	
if __name__ == "__main__":
	source = r"c:\target.py"
	target = r"m:\target.py"
	syncfile = create_SyncFile(source,target)
	print is_sync_outdated(syncfile.source,syncfile.target)

	# synchronize(syncfile)
	
	# comp = filecmp.dircmp("C:\\sync2","c:\\sync")
	# print comp.common_files
