#!/usr/bin/python
# -*- coding: UTF-8 -*-
# A tool for parsing Combined Log Files.
import sys,re,os,socket

#COLOURZ
RED='\033[1;31m'
BLU='\033[1;34m'
CLR='\033[0m'

me="Lé Parser"
usage="cat <file> | %prog"

class Parse:
	def ua(self,inLine):
		return self.inLine.split('"')[5]

	def refs(self,inLine):
		return self.inLine.split('"')[3]

	def ips(self,inLine):
		self.inLine=inLine
		check=re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
		for ip in check.findall(inLine):
			return ip
	
	def errs(self,inLine):
		self.inLine=inLine
		check=re.compile(r'HTTP/\d.\d" \d+')
		for err in check.findall(inLine):
			return err[-3:]

def countThing(things):
	hits=[(things.count(thing), thing) for thing in set(things)]
	ehits=[]
	[ehits.append(hit) for hit in hits]
	return sorted(ehits,reverse=True)[:10]

def retList(thing):
	thing=sorted(thing,reverse=True)[:10]
	return countThing(thing)

def main():
	print("{0} - Jinsku".format(me))
	ips=[];errs=[];uas=[];refs=[];bots=[]
	parser=Parse()
	read=sys.stdin ## normal stdin and readlines() allow for arbitrary code exec, so we're sanitizing it
	lines=(line.replace('\t','').replace('\n','') for line in read.readlines())
	for line in lines:
		try:
			if parser.ips(line) is not None: ips.append(parser.ips(line))
			if parser.errs(line) is not None: errs.append(parser.errs(line))
			if parser.ua(line) is not None: uas.append(parser.ua(line))
			if parser.refs(line) is not None: refs.append(parser.refs(line))
		except: print("usage: "+usage);exit(1)

	#print top 10 IPs
	print("\n["+BLU+"+"+CLR+"] Top IPs")
	ips=retList(ips)
	for ip in ips: print("\t{} {} - {}".format(ip[0],ip[1],socket.getfqdn(ip[1])))

	#print top 10 errs
	print("\n["+BLU+"+"+CLR+"] Top Response Codes")
	errs=retList(errs)
	for err in errs: print("\t{} {}".format(err[0],err[1]))

	#print top 10 uas
	print("\n["+BLU+"+"+CLR+"] Top User Agents")
	uas=retList(uas)
	for ua in uas: print("\t{} {}".format(ua[0],ua[1]))

	#print top 10 refs
	print("\n["+BLU+"+"+CLR+"] Top Referrers")
	refs=retList(refs)
	for ref in refs: print("\t{} {}".format(ref[0],ref[1]))
	print("")

if __name__=="__main__":
	main()
