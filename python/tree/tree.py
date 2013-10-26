#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       experiment.py
#       
#       Copyright 2013 Jelle Smet
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

import re
import string
import random
import pprint
import pickle
import sys
import time
import hashlib

def generateRules(rules=20, min_rule_length=5, max_rule_length=10, max_rule_value=5):
	base=["one","two","three","four","five","six","seven","eight","nine","zero"]
	ruleset={}
	for rule in xrange(rules):
		for name in base:
			ruleset["%s-%s"%(rule,name)]={ random.choice(string.ascii_lowercase):random.randint(0,max_rule_value) for blah in xrange(random.randint(min_rule_length, max_rule_length)) }
	return ruleset

def convert(rules):
	converted={}
	for rule in rules:
		for name in rules[rule]:
			if converted.has_key(name):
				if converted[name].has_key(rules[rule][name]):
					converted[name][rules[rule][name]].append((rule,len(rules[rule])))
				else:
					converted[name][rules[rule][name]]=[(rule,len(rules[rule]))]
			else:
				converted[name]={rules[rule][name]:[(rule,len(rules[rule]))]}
	
	print converted
	#within each field sort which condition is requested the most
	for item in converted:
		converted[item] = sorted([ (key,converted[item][key]) for key in converted[item] ], key=lambda value: len(value[1]), reverse=True)

	#sort all fields on the total number of defined conditions
	return sorted(converted.iteritems(), key=lambda value: sum(len(v[1]) for v in value[1]), reverse=True)

def generateData(length=10000, min_rule_length=5, max_rule_length=10, max_rule_value=5):
	for x in xrange(length):
		yield { random.choice(string.ascii_lowercase):random.randint(0,max_rule_value) for blah in xrange(random.randint(min_rule_length,max_rule_length)) }

def mapMatch(rulenames, map, data):
	state={x:0 for x in rulenames}
	for field in map:
		if field[0] in data:			
			for match in field[1]:
				if match[0] == data[field[0]]:					
					for rule in match[1]:
						state[rule[0]]+=1
						if rule[1] == state[rule[0]] and state[rule[0]] <= len(data):
							return "Rule %s matches."%(rule[0])
	return False

def sequentialMatch(rules, data):
	#sys.exit()
	#print data
	#print rules
	for rule in rules:
		hits=0
		for match in rules[rule]:
			if data.has_key(match) and data[match] == rules[rule][match]:
				hits+=1
				if hits == len(rules[rule]):
					return "Rule %s matches."%(rule)	
	return False

def generateDataSets():
	#pp = pprint.PrettyPrinter(indent=4)
	#pp.pprint(cruleset)
	ruleset=generateRules(rules=1, min_rule_length=3, max_rule_length=7)
	data=[x for x in generateData(length=100000, min_rule_length=3, max_rule_length=7)]
	return (ruleset, data)

def main():
	#print ruleset
	(ruleset, data)=generateDataSets()

	# mapMatch method
	#################

	cruleset=convert(ruleset)
	ruleset_keys=ruleset.keys()

	print cruleset
	sys.exit()

	print "mapMatch:"
	mm_hash=hashlib.md5()
	start=time.time()
	for line in data:
		mm=mapMatch(ruleset_keys, cruleset, line)
		if mm != False:
			mm_hash.update(mm)
	print time.time()-start
	print mm_hash.hexdigest()
	print ("")

	print "sequentialMatch:"
	sm_hash=hashlib.md5()
	start=time.time()
	for line in data:
		sm=sequentialMatch(ruleset, line)
		if sm != False:
			sm_hash.update(sm)
	print time.time()-start
	print sm_hash.hexdigest()

if __name__ == '__main__':
	main()
