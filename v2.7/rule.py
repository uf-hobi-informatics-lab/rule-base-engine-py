#coding:utf-8
###
 # <p>Title:  </p>
 # <p>Create Date: 16:08:25 06/12/2012</p>
 # <p>Copyright: Copyright (c) Department of Biomedical Informatics </p>
 # <p>Company: Vanderbilt University </p>
 # @author Buzhou Tang
 # @version 1.0
 # <p>Description: 
 #		python rule.py ruledir patterndir
 #			  parse rules listed in the directory rules according topatterns in the directory patterns
 # </p>
 ##

import sys
import string
import re
import os

from temporalExpression import *

class Rule:
	# for example, Year4Digit:[12]\d{2}
	# all patterns are formated as: key:value[|value]
	pattern = {}
	#for example, "NormMoth: jan 01"
	# all patterns are formated as: key:{subkey,value}
	norm_pattern = {}
	def __init__(self, rule_str='', type='DATE'):
		self.type = type
		self.expression = ''
		self.attribute = {}
		if rule_str == '':
			return
		else:
			# the blank is prohibit between two attributes
			token = rule_str.split('",')
			for item in token:
				(attr, val) = item.split('="')
				val = val.strip('"')
				if attr == 'expression':
					# parse patterns in the expression
					self.expression = re.sub(r'%(\w+)', lambda m: '(' + Rule.pattern[m.group(1)] + ')', val)
				else:
					self.attribute[attr] = val
	
	def apply(self, input_str = ''):
		if input_str == '':
			print 'no input string!'
			return None
		te = []
		for m in re.finditer(self.expression, input_str):
			if ((m.start() > 0) and (input_str[m.start()-1] not in [' ', '\t'])) or ((m.end() < len(input_str)) and (input_str[m.end()] not in [' ', '\t'])):
			#	print input_str[m.start():m.end()]
				continue
			tmp_te = TemporalExpression()
			tmp_te.type = rule.type
			tmp_te.start = m.start()
			tmp_te.end = m.end()
			tmp_te.text = input_str[tmp_te.start:tmp_te.end]
			tmp_te.word_start = len(re.findall(r'\s+', input_str[0: tmp_te.start]))
			tmp_te.word_end = tmp_te.word_start + len(re.findall(r'\s+', tmp_te.text)) + 1
			
			for attr in self.attribute:
				if attr == 'val':
					# parse 'group' information
					tmp_te.value = re.sub(r'group\((\d+)\)', lambda n:m.group(int(n.group(1))), self.attribute[attr])
					# parse normal patterns in value
					tmp_te.value = re.sub(r'%(\w+)\((.*?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.value)
				if attr == 'mod':
					# parse 'group' information
					tmp_te.mod = re.sub(r'group\((\d+)\)', lambda n:m.group(int(n.group(1))), self.attribute[attr])
					# parse mod patterns in mod
					#tmp_te.mod = re.sub(r'%(\w+)\((\w+[\w+-]+\w+|\w+\.?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.mod)
					tmp_te.mod = re.sub(r'%(\w+)\((.*?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.mod)
			te.append(tmp_te)
		return te
	
	def apply2section(self, sec_type = 'ADMISSION', input_sec = [], start = 0):
		if input_sec == []:
			print 'no input section!'
			return None
		te = []
		row_num = start
		#print self.expression
		for line in input_sec:
			for m in re.finditer(self.expression, line):
				if ((m.start() > 0) and (line[m.start()-1] not in [' ', '\t'])) or ((m.end() < len(line)) and (line[m.end()] not in [' ', '\t'])):
					continue
				tmp_te = TemporalExpression()
				tmp_te.sec = sec_type
				tmp_te.row = row_num
				tmp_te.type = self.type
				tmp_te.start = m.start()
				tmp_te.end = m.end()
				tmp_te.text = line[tmp_te.start:tmp_te.end]
				tmp_te.word_start = len(re.findall(r'\s+', line[0: tmp_te.start]))
				tmp_te.word_end = tmp_te.word_start + len(re.findall(r'\s+', tmp_te.text)) + 1
				for attr in self.attribute:
					if attr == 'val':
						# parse 'group' information
						tmp_te.value = re.sub(r'group\((\d+)\)', lambda n:m.group(int(n.group(1))), self.attribute[attr])
						# parse normal patterns in value
						#print tmp_te.value
						#m = re.findall(r'%(\w+)\(((.*?))\)', tmp_te.value)
						#print m
						#tmp_te.value = re.sub(r'%(\w+)\((\w+[\w+-]+\w+|\w+\.?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.value)
						# not greedy pattern
						tmp_te.value = re.sub(r'%(\w+)\((.*?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.value)
						#print tmp_te.value
					if attr == 'mod':
						# parse 'group' information
						tmp_te.mod = re.sub(r'group\((\d+)\)', lambda n:m.group(int(n.group(1))), self.attribute[attr])
						# parse mod patterns in mod
						#tmp_te.mod = re.sub(r'%(\w+)\((\w+[\w+-]+\w+|\w+\.?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.mod)
						tmp_te.mod = re.sub(r'%(\w+)\((.*?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.mod)
				te.append(tmp_te)
			row_num += 1
		return te
	
	def apply2file(self, infile = ''):
		if infile == '':
			print 'no input file!'
			return None
		te = []
		row_num = 0
		for line in file(infile):
			row_num += 1
			line = line.strip(None)
			if line == '':
				continue
			for m in re.finditer(self.expression, line):
				tmp_te = TemporalExpression()
				tmp_te.row = row_num
				tmp_te.type = rule.type
				tmp_te.start = m.start()
				tmp_te.end = m.end()
				tmp_te.text = line[tmp_te.start:tmp_te.end]
				tmp_te.word_start = len(re.findall(r'\s+', line[0: tmp_te.start]))
				tmp_te.word_end = tmp_te.word_start + len(re.findall(r'\s+', tmp_te.text)) + 1
				for attr in self.attribute:
					if attr == 'val':
						# parse 'group' information
						tmp_te.value = re.sub(r'group\((\d+)\)', lambda n:m.group(int(n.group(1))), self.attribute[attr])
						# parse normal patterns in value
						#tmp_te.value = re.sub(r'%(\w+)\((\w+[\w+-]+\w+|\w+)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.value)
						tmp_te.value = re.sub(r'%(\w+)\((.*?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.value)
					if attr == 'mod':
						# parse 'group' information
						tmp_te.mod = re.sub(r'group\((\d+)\)', lambda n:m.group(int(n.group(1))), self.attribute[attr])
						# parse mod patterns in mod
						#tmp_te.mod = re.sub(r'%(\w+)\((\w+[\w+-]+\w+|\w+)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.mod)
						tmp_te.mod = re.sub(r'%(\w+)\((.*?)\)', lambda n: Rule.norm_pattern[n.group(1)][n.group(2).lower()], tmp_te.mod)
				te.append(tmp_te)
		return te

	# load patterns
	@staticmethod
	def loadPattern(pattern_dir = ''):
		tmpdir = pattern_dir
		if not tmpdir.endswith('/'):
			tmpdir += '/'
		for fi in os.listdir(tmpdir):
			fi = tmpdir + fi
			if os.path.isdir(fi):
				Rule.loadPattern(fi)
			else:
				tmp_pattern = []
				cur_pattern = ''
				for line in file(fi):
					line = line.strip()
					if line == '' or line.startswith('#') or line.startswith('//'):
						continue
					if line.endswith(':'):
						if cur_pattern != '':
							Rule.pattern[cur_pattern] = '|'.join(tmp_pattern)
						tmp_pattern = []
						cur_pattern = line[:-1].strip()
					else:
						tmp_pattern.append(line)
				if (cur_pattern != '') and tmp_pattern:
					Rule.pattern[cur_pattern] = '|'.join(tmp_pattern)
	
	# load normal patterns
	@staticmethod
	def loadNormPattern(norm_dir = ''):
		tmpdir = norm_dir
		if not tmpdir.endswith('/'):
			tmpdir += '/'
		for fi in os.listdir(tmpdir):
			fi = tmpdir + fi
			if os.path.isdir(fi):
				Rule.loadNormPattern(fi)
			else:
				cur_pattern = ''
				for line in file(fi): 
					line = line.strip()
					if line == '' or line.startswith('#') or line.startswith('//'):
						continue
					if line.endswith(':'):
						cur_pattern = line[:-1].strip()
						if cur_pattern != '':
							Rule.norm_pattern[cur_pattern] =  {}
					else:
						if cur_pattern == '':
							print 'none norm pattern'
							return
						#token = line.split(None)
						token = line.split('=>')
						Rule.norm_pattern[cur_pattern][token[0]] = token[1]

if __name__ == "__main__":

	if(len(sys.argv)<4):
		print ''' No enough parameter!\n
				  Uasage: python2.7 rule.py patternpath normal_patternpath inputfile [outputfile]'''
		sys.exit()
	pafname = sys.argv[1]
	normfname = sys.argv[2]
	infname = sys.argv[3]
	ofname = ''
	if len(sys.argv) == 4:
		ofname = infname.split('/')[-1].split('.')[0] + '.timex'
	else:
		ofname = sys.argv[4]
	
	Rule.loadPattern(pafname)
	Rule.loadNormPattern(normfname)
	print Rule.norm_pattern
	for item in Rule.pattern:
		print item, '=>', Rule.pattern[item]
	rule_str = 'expression="%MonthWord (%DayWord|%DayNumber)",val="UNDEF-year-%NormMonth(group(1))-%NormDay(group(2))"'
	#rule_str = 'expression="%Year4Digit-%MonthNumber-%DayNumber",val="group(1)-group(2)-group(3)"'
	rule_str1 = 'expression="%MonthNumber-%DayNumber-%Year2Digit",val="UNDEF-centurygroup(3)-%NormMonth(group(1))-%NormDay(group(2))",mod="%Mod(over)"'
	#input_str = 'at 2010-01-29 , we had a meeting . posted time : 1-09-10'
	input_str = 'February 25th'
	rule = Rule(rule_str)
	print 'rule: ', rule.expression
	rule1 = Rule(rule_str1)
	print 'rule1: ', rule1.expression
	te = rule.apply(input_str)
	te += rule1.apply(input_str)
	#word_index = []
	#seperator_index = []
	#seperator_index.append(0)
	#for m in re.finditer(r'\s+', input_str):
	#	seperator_index.append(m.start())
	#	seperator_index.append(m.end())
	#seperator_index.append(len(input_str))
	#print seperator_index

	#te = rule.apply2file(infname)
	for tmp_te in te:
		print tmp_te.tostring()
	
	#fo = open(ofname,'w')

	#fo.close()

