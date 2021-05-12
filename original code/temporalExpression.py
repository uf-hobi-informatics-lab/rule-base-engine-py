#coding:utf-8
###
 # <p>Title:  </p>
 # <p>Create Date: 10:30:21 06/12/2012</p>
 # <p>Copyright: Copyright (c) Department of Biomedical Informatics </p>
 # <p>Company: Vanderbilt University </p>
 # @author Yonghui Wu, Buzhou Tang
 # @version 1.0
 # <p>Description: 
 #	temporal expression
 # </p>
 ##
import sys
import string

te_type = ['DATE', 'TIME', 'DURATION', 'FREQUENCY']
mod_type = ['NA', 'MORE', 'LESS', 'APPROX', 'START', 'END', 'MIDDLE']
class TemporalExpression:
	def __init__(self):
		# section
		self.sec = 'ADMISSION'
		# context in [self.start, self.end) in self.row 
		self.text = ''
		# starts from 1
		self.row = 0
		# starts from 0
		# character index of the start and end
		self.start = -1
		self.end = -1
		# word index of the start and the end
		self.word_start = -1
		self.word_end = -1
		self.value = ''
		self.type = 'DATE'
		self.mod = 'NA'

	# 0 represents using character index; 1 represents using word index
	def tostring(self, type = 0):
		te_str = 'TIMEX3="' 
		te_str += self.text + '" '
		if type == 0:
			te_str += str(self.row) + ':' + str(self.start) + ' ' + str(self.row) + ':' + str(self.end)
		elif type ==1:
			te_str += str(self.row) + ':' + str(self.word_start) + ' ' + str(self.row) + ':' + str(self.word_end)
		te_str += '||' + 'type="' + self.type + '"'
		te_str += '||' + 'val="' + self.value + '"'
		te_str += '||' + 'mod="' + self.mod + '"'
		return te_str

se_te_type = ['ADMISSION', 'DISCHARGE']
class SectionTemporalExpression:
	def __init__(self):
		# context in [self.start, self.end) in self.row 
		self.text = ''
		# starts from 1
		self.row = 0
		# starts from 0
		# character index of the start and end
		self.start = -1
		self.end = -1
		# word index of the start and the end
		self.word_start = -1
		self.word_end = -1
		self.type = 'ADMISSION'
		self.value = ''

	# 0 represents using character index; 1 represents using word index
	def tostring(self, type = 0):
		te_str = 'SECTIME="' 
		te_str += self.text + '" '
		if type == 0:
			te_str += str(self.row) + ':' + str(self.start) + ' ' + str(self.row) + ':' + str(self.end)
		elif type ==1:
			te_str += str(self.row) + ':' + str(self.word_start) + ' ' + str(self.row) + ':' + str(self.word_end)
		te_str += '||' + 'type="' + self.type + '"'
		te_str += '||' + 'dvalue="' + self.value + '"'
		return te_str
