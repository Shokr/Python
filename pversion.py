################################################
# pversion
#
# This module is used for getting and setting v000 in paths, also listing versions in a directory is possble
#
# Developed by : Sven Fraeys
#
# Contact : sven.fraeys@gmail.com
#
# All Rights Reserved, Free for non-commercial use, for use please contact the developer
#
################################################
import re
import os

version_prefix = "v"	

def integer_to_string(number,digits=3):
		'''
			converts a number to 12 to '012' string
		'''
		numberStr = str(number)
		numberOfDigits = len(numberStr)
		numberOfDigitsToAdd = digits - numberOfDigits
		returnStr = ""
		for i in range(numberOfDigitsToAdd):
			returnStr += "0"
		returnStr += numberStr
		return returnStr
def string_to_integer(versionString):
	return int(versionString[1:])

def create_version_string(version):
	return version_prefix+integer_to_string(version)
	
def get_version_string(path):
	versionMatch = re.search(version_prefix+"\d\d\d",path)
	if versionMatch == None:
		return None
	return versionMatch.group()

def get_version_number_string(path):
	versionstring = get_version_string(path)
	if versionstring == None:
		return None
	versionMatch = re.search("\d\d\d",versionstring)
	if versionMatch == None:
		return None
	return versionMatch.group()
	
def get_version_integer(path):
	versionnumberstring = get_version_number_string(path)
	if versionnumberstring is None:
		return None
	return int(versionnumberstring)
	
def set_version(path,version):
	versioninteger = get_version_integer(path)
	if versioninteger == None:
		return None
	
	newversionstring = create_version_string(version)
	originalversionstring = get_version_string(path)
	return path.replace(originalversionstring, newversionstring)
	
	# versioninteger += ""
def next_version(path):
	version = get_version_integer(path)
	newversion = version + 1
	return set_version(path,newversion)
	
def previous_version(path):
	version = get_version_integer(path)
	newversion = version - 1
	return set_version(path,newversion)
	
def remove_version(path):
	versionMatch = re.search("_"+version_prefix+"\d\d\d",path)
	if versionMatch != None:
		return path.replace(versionMatch.group(),"")
		
	versionMatch = re.search(version_prefix+"\d\d\d",path)
	if versionMatch != None:
		return path.replace(versionMatch.group(),"")
	return path

def list_versions(path):
	directory = os.path.dirname(path)
	basename = os.path.basename(path)
	files = os.listdir(directory)
	noVersionSource = remove_version(basename).lower()
	returnFiles = []
	for file in files:
		noVersionTarget = remove_version(file).lower()
		
		if noVersionSource == noVersionTarget:
			returnFiles.append( os.path.normpath(os.path.join(directory, file) ) )
			
	return returnFiles

def last_version(path):
	versionList = list_versions(path)
	highestExistingVersionInteger = -1
	highestExistingVersionPath = None
	for version in versionList:
		versionInteger = get_version_integer(version)
		if versionInteger > highestExistingVersionInteger:
			highestExistingVersionInteger = versionInteger
			highestExistingVersionPath = version
			
	return highestExistingVersionPath
def new_version(path):
	lastversionPath = last_version(path)
	if lastversionPath == None:
		return path
	lastversionInteger = get_version_integer(lastversionPath)
	newversionInteger = lastversionInteger + 1
	return os.path.normpath(set_version(lastversionPath, newversionInteger))
	
def list_directory_as_highest_dictionary(path):
	'''
		list all unique paths with last versions
	'''
	files = os.listdir(path)
	uniqueDictionary = {}
	for file in files:
		filenoVersion = remove_version(file)
		if filenoVersion not in uniqueDictionary:
			uniqueDictionary[filenoVersion] = file
		else:
			versionfile = get_version_integer(file)
			versionhighest = get_version_integer(uniqueDictionary[filenoVersion])
			if versionfile > versionhighest:
				uniqueDictionary[filenoVersion] = file
				
	return uniqueDictionary

def list_directory_lastversions(path):
	uniqueDictionary = list_directory_as_highest_dictionary(path)
	returnArray = []
	
	for key in uniqueDictionary:
		returnArray.append(uniqueDictionary[key])
		
	return returnArray
	
def directory_list_versions(path):
	versionsArray = []
	for filename in os.listdir(path):
		versionString = get_version_string(filename)
		if versionString: versionsArray.append(os.path.join(path,filename))

	# versions = list_versions(path)
	return versionsArray
	
if __name__ == "__main__":
	print last_version("c:/vers/")
	
		
