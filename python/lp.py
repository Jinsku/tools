#!/usr/bin/python
# -*- coding: UTF-8 -*-
# A tool for parsing Combined Log Files.
# TODO:
# Add starting end ending time/date
# Add bandwidth usage
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
	return sorted(ehits,reverse=True)

def retList(thing):
	thing=sorted(thing,reverse=True)
	return countThing(thing)

def main():
	print("{0} - Jinsku".format(me))
	ips=[];errs=[];uas=[];refs=[];bots=[]
	parser=Parse()
	read=sys.stdin ## normal stdin and readlines() allow for arbitrary code exec, so we're sanitizing it
	lines=(line.replace('\t','').replace('\n','') for line in read.readlines())
	total_lines=0
	for line in lines:
		try:
			if parser.ips(line) is not None: ips.append(parser.ips(line))
			if parser.errs(line) is not None: errs.append(parser.errs(line))
			if parser.ua(line) is not None: uas.append(parser.ua(line))
			if parser.refs(line) is not None: refs.append(parser.refs(line))
			total_lines+=1
		except: print("usage: "+usage);exit(1)

	print("\n["+BLU+"+"+CLR+"] Summary") #Prints summary
	print("{:>4}{:<36}: {}".format("","Total number of unique IPs",len(countThing(ips))))
	print("{:>4}{:<36}: {}".format("","Total number of requests",total_lines))
	print("{:>4}{:<36}: {}".format("","Total number of unique user agents",len(countThing(uas))))
	print("{:>4}{:<36}: {}".format("","Total number of unique referrers",len(countThing(refs))))

	print("\n["+BLU+"+"+CLR+"] Top IPs") #Prints top 10 IPs
	ips=retList(ips)[:10]
	for ip in ips: print("{:>6} {:<15} - {:<15}".format(ip[0],ip[1],socket.getfqdn(ip[1])))

	print("\n["+BLU+"+"+CLR+"] Top Response Codes") #Print top 10 errs
	errs=retList(errs)[:10]
	for err in errs: print("{:>6} {}".format(err[0],err[1]))

	print("\n["+BLU+"+"+CLR+"] Top User Agents") #Print top 10 UAs
	uas=retList(uas)[:10]
	for ua in uas: print("{:>6} {}".format(ua[0],ua[1]))

	print("\n["+BLU+"+"+CLR+"] Top Referrers") #Print top 10 refs
	refs=retList(refs)[:10]
	for ref in refs: print("{:>6} {}".format(ref[0],ref[1]))
	print("")

if __name__=="__main__":
	main()
