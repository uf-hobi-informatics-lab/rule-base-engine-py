###
 # <p>Title:  </p>
 # <p>Create Date: 14:54:36 06/18/2012</p>
 # <p>Copyright: Copyright (c) Department of Biomedical Informatics </p>
 # <p>Company: Vanderbilt University </p>
 # @author Buzhou Tang
 # @version 1.0
 # <p>Description: 
 #		python getTimexFromExtent.py dir outfile
 #		get timex3 phrases from *.extent files in dir recursively
 # </p>
 ##
import sys
import string
import os

# get timex3 phrases from *.extent files in the inputdir recursively.
def getTimexFromExtent(inputdir, fo):
	tmpdir = inputdir
	for fi in os.listdir(tmpdir):
		if not tmpdir.endswith('/'):
			tmpdir = tmpdir + '/'
		if os.path.isdir(tmpdir + fi):
			#print 'dirlist:', tmpdir + fi
			getTimexFromExtent(tmpdir + fi, fo)
		elif os.path.isfile(tmpdir + fi) and fi.endswith('.extent'):
			#print 'filelist:', tmpdir + fi
			fo.write('File:' + tmpdir + fi + '\n')
			for line in file(tmpdir + fi):
				if line.startswith('TIMEX3=') or line.startswith('SECTIME='):
					fo.write(line)

if __name__ == "__main__":

	if(len(sys.argv)<3):
		print ''' No enough parameter!\n
				  Uasage: python getTimexFromExtent.py dir outfile
				  get timex3 phrases from *.extent files in dir recursively'''
		sys.exit()
	
	fo = open(sys.argv[2], 'w+')
	getTimexFromExtent(sys.argv[1], fo)
	fo.close


