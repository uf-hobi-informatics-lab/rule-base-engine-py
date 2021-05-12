###
 # <p>Title:  </p>
 # <p>Create Date: 10:38:36 05/02/2012</p>
 # <p>Copyright: Copyright (c) Department of Biomedical Informatics </p>
 # <p>Company: Vanderbilt University </p>
 # @author Buzhou Tang
 # @version 1.0
 # <p>Description: 
 #		python mergefilesInDirByRow.py dir outfile [suffix]
 #		merge files in the dir [with suffix] by row recursively
 # </p>
 ##
import sys
import string
import os

# merge files in the inputdir by row recursively.
def mergefilesInDirByRow(inputdir, fo, suffix = ''):
	tmpdir = inputdir
	for fi in os.listdir(tmpdir):
		if not tmpdir.endswith('/'):
			tmpdir = tmpdir + '/'
		if os.path.isdir(tmpdir + fi):
			#print 'dirlist:', tmpdir + fi
			mergefilesInDirByRow(tmpdir + fi, fo, suffix)
		elif os.path.isfile(tmpdir + fi) and fi.endswith(suffix):
			#print 'filelist:', tmpdir + fi
			for line in file(tmpdir + fi):
				fo.write(line)

if __name__ == "__main__":

	if(len(sys.argv)<3):
		print ''' No enough parameter!\n
				  Uasage: python mergefilesInDirByRow.py dir outfile [suffix]
				  merge files with suffix in dir by row recursively'''
		sys.exit()
	
	fo = open(sys.argv[2], 'w+')
	suffix = ''
	if len(sys.argv) == 4:
		suffix = sys.argv[3]
	mergefilesInDirByRow(sys.argv[1], fo, suffix)
	fo.close
