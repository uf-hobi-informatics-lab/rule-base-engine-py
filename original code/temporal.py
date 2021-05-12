#coding:utf-8
###
 # <p>Title:  </p>
 # <p>Create Date: 10:30:21 06/12/2012</p>
 # <p>Copyright: Copyright (c) Department of Biomedical Informatics </p>
 # <p>Company: Vanderbilt University </p>
 # @author Yonghui Wu, Buzhou Tang
 # @version 1.0
 # <p>Description:
 #		Uasage: python temporal.py patterndir normdir ruledir inputfile [outputfile]
 #			  temporal expression extraction and normalization
 # </p>
 ##

import sys
import string
import re
from temporalExpression import *
from rule import *
from note import *

def loadRule(rule_dir, rules):
	tmpdir = rule_dir
	if not tmpdir.endswith('/'):
		tmpdir += '/'
	for fi in os.listdir(tmpdir):
		fi = tmpdir + fi
		if os.path.isdir(fi):
			Rule.loadRule(fi)
		else:
			cur_type = ''
			for line in file(fi):
				line = line.strip()
				if line == '' or line.startswith('#') or line.startswith('//'):
					continue
				if line.endswith(':'):
					cur_type = line[:-1].strip()
				else:
					if cur_type == '':
						print 'none type'
						return
					rules.append(Rule(line, cur_type))

# filt temporal expressions those covered by others at note-level.
def teFilter(te):
	# (row:start, [row:end, index])
	te_max = {}
	te_available = [0] * len(te)
	for i in range(0, len(te)):
		if (str(te[i].row) + ':' + str(te[i].start)) not in te_max:
			te_max[str(te[i].row) + ':' + str(te[i].start)] = [0]*2
			te_max[str(te[i].row) + ':' + str(te[i].start)][0] = te[i].end
			te_max[str(te[i].row) + ':' + str(te[i].start)][1] = i
			te_available[i] = 1
		elif te[i].end > te_max[str(te[i].row) + ':' + str(te[i].start)][0]:
			te_max[str(te[i].row) + ':' + str(te[i].start)][0] = te[i].end
			te_available[te_max[str(te[i].row) + ':' + str(te[i].start)][1]] = 0
			te_max[str(te[i].row) + ':' + str(te[i].start)][1] = i
			te_available[i] = 1
	
	new_te = []
	for i in range(0, len(te)):
		if te_available[i] == 1:
			new_te.append(te[i])
	
	return new_te


if __name__ == "__main__":

	if(len(sys.argv)<5):
		print ''' No enough parameter!\n
				  Uasage: python2.7 temporal.py patterndir normdir ruledir inputfile [outputfile]'''
		sys.exit()
	infname = sys.argv[4]
	ofname = ''
	if len(sys.argv) == 5:
		ofname = infname.split('/')[-1].split('.')[0] + '.timex'
	else:
		ofname = sys.argv[5]

	Rule.loadPattern(sys.argv[1])
	Rule.loadNormPattern(sys.argv[2])
	
	rules = []
	loadRule(sys.argv[3], rules)
##	print 'rules:'
##	for rule in rules:
##		rule_str = ''
##		rule_str += 'expression="' + rule.expression + '"'
##		rule_str += ',type="' + rule.type + '"'
##		for attr in rule.attribute:
##			rule_str += ',' + attr + '="' + rule.attribute[attr] + '"'
##		print rule_str
	
	note = Note(infname)
	te = []
	sec_te = []
	for section in note.sec:
		tmp_te = []
		for rule in rules:
			tmp_te += rule.apply2section(section.type, section.context, section.start)
		tmp_te = teFilter(tmp_te)
		if (section.type in se_te_type) and tmp_te:
			tmp_sec_te = SectionTemporalExpression()
			tmp_sec_te.text = tmp_te[0].text
			tmp_sec_te.row = tmp_te[0].row
			tmp_sec_te.start = tmp_te[0].start
			tmp_sec_te.end = tmp_te[0].end
			tmp_sec_te.word_start = tmp_te[0].word_start
			tmp_sec_te.word_end = tmp_te[0].word_end
			tmp_sec_te.type = section.type
			tmp_sec_te.value = tmp_te[0].value
			sec_te.append(tmp_sec_te)
		te += tmp_te
			
	for item in te:
		print item.tostring(1)
	for item in sec_te:
		print item.tostring(1)
	
	#fo = open(ofname,'w')

	#fo.close()

