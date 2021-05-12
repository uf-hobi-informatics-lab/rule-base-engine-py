#coding:utf-8
###
 # <p>Title:  </p>
 # <p>Create Date: 10:30:21 06/12/2012</p>
 # <p>Copyright: Copyright (c) Department of Biomedical Informatics </p>
 # <p>Company: Vanderbilt University </p>
 # @author Buzhou Tang
 # @version 1.0
 # <p>Description: 
 #		python note.py inputfile
 #		clinic note representation
 # </p>
 ##

import sys
import string
import re
from temporalExpression import *

sec_type = {'undef':'UNDEF', 'discharge':'DISCHARGE', 'admission':'ADMISSION', 'history':'HISTORY_OF_PRESENT_ILLNESS', 'hospital course':'HOSPITAL_COURSE'}

class Section:
	def __init__(self):
		self.type = sec_type['undef']
		self.start = 1
		self.context = []

	def add(self, line):
		self.context.append(line)

	def is_empty(self):
		if self.context:
			return False
		else:
			return True

class Note:
	def __init__(self, fnote = ''):
		self.sec = []
		if fnote == '':
			return
		cur_sec = Section()
		row_num = 0
		for line in file(fnote):
			line = line.strip()
			row_num += 1
			if re.match(r'^admission date.*:', line, re.I):
				if not cur_sec.is_empty():
					self.sec.append(cur_sec)
				cur_sec = Section()
				cur_sec.type = sec_type['admission']
				cur_sec.start = row_num
				cur_sec.add(line)
			elif re.match(r'^discharge date.*:', line, re.I):
				if not cur_sec.is_empty():
					self.sec.append(cur_sec)
				cur_sec= Section()
				cur_sec.type = sec_type['discharge']
				cur_sec.start = row_num
				cur_sec.add(line)
			elif re.match(r'((^history of (the )?present illness)|(^HPI)|(^history / reason for hospitalization)).*:', line, re.I):
				if not cur_sec.is_empty():
					self.sec.append(cur_sec)
				cur_sec= Section()
				cur_sec.type = sec_type['history']
				cur_sec.start = row_num
				cur_sec.add(line)
			elif re.match(r'^(brief )?(summary of )?hospital course.*:', line, re.I):
				if not cur_sec.is_empty():
					self.sec.append(cur_sec)
				cur_sec = Section()
				cur_sec.type = sec_type['hospital course']
				cur_sec.start = row_num
				cur_sec.add(line)
			else:
				cur_sec.add(line)
		if not cur_sec.is_empty():
			self.sec.append(cur_sec)
			
	def getSectionFromRowNum(self, row_num):
		section_type = ''
		if row_num < 1:
			return section_type
		for item in self.sec:
			if item.start <= row_num:
				section_type = item.type
			else:
				break
		return section_type
	
	def getSentenceFromRowNum(self, row_num):
		Sentence = ''
		if row_num < 1:
			return sentence
		sec_index = -1
		for item in self.sec:
			if item.start > row_num:
				break
			sec_index += 1
		return self.sec[sec_index].context[row_num - self.sec[sec_index].start]

	def print_sec(self):
		for section in self.sec:
			print 'section type:', section.type
			print 'row num:', section.start
			print '\n'.join(section.context)

if __name__ == "__main__":

	if(len(sys.argv)<2):
		print ''' No enough parameter!\n
				  Uasage: python2.7 note.py inputfile'''
		sys.exit()
	infname = sys.argv[1]
	note = Note(infname)
	note.print_sec()
	print note.getSectionFromRowNum(2)

	#fo = open(ofname,'w')

	#fo.close()

