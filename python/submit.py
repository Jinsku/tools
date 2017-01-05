#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/smtplib.html
import sys,os,hashlib,time,socket,smtplib,getpass,logging
if sys.version_info[0] <3:
	print("Requires Python3")
	exit(1)

#COLOURZ
GRN='\033[1;32m'
WHITE='\033[1;37m'
RED='\033[1;31m'
BLU='\033[1;36m'
CLR='\033[0m'

config={
'sender':'', #Will attempt to generate if no sender present
'to':[], #Expects a list
}

def log(malware,message,submitted):
	log=os.path.expanduser("~")+"/logs/submit.log"
	logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s')
	if submitted==True:
		logging.info("{} {}".format(malware,message))
	elif submitted==False:
		logging.warning("{} {}".format(malware,message))
	else:
		logging.warning("Invalid log entry")

def getSender():
	user=getpass.getuser()
	hostname=socket.getfqdn(socket.gethostname())
	return user+"@"+hostname

def sendMe(malware):
	hostname=socket.getfqdn(socket.gethostname())
	ltime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
	if config["sender"] == None or config["sender"] == '':
		config["sender"]=getSender()
	subject="File report for {} - {}".format(hostname,ltime)
	header="From: {}\r\nTo: ".format(config["sender"])
	for user in config["to"]:
		header+="{},".format(user)
	header+="\r\nSubject: {}\r\n\r\n".format(subject)
	contents=header+"Greetings!\n\nOne or more files have been submitted for your review on {} at the paths included below\n\n".format(hostname)
	for mal in malware:
		contents+="{:>15} {:>4}\n".format("======",mal["path"])
		contents+="{:>15}: {:>4}\n".format("Time",mal["mtime"])
		contents+="{:>15}: {:>4}\n".format("SHA256 Hash",mal["sha256"])
		contents+="{:>15}: {:>4}\n\n".format("Sample",str(mal["sample"]))
	try:
		with smtplib.SMTP('localhost') as smtp:
			smtp.sendmail(config["sender"],config["to"],contents)	
			log(mal["path"],"submitted successfully.",True)
			return True
	except:
		log(mal["path"],"failed to submit.",False)
		return False

def getHash(thing):
	with open(thing,"r") as fd:
		sha=hashlib.sha256(fd.read().encode("utf-8")).hexdigest()
	return sha

def getTime(thing):
	get=os.path.getmtime(thing)
	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(get))

def main():
	files=[]
	if len(sys.argv)>1:
		for arg in sys.argv[1:]:
			files.append(os.path.abspath(arg))
	else:
		print("No files provided")
		exit(1)
	try:
		malware=[]
		for thing in files:
			info={}
			if os.path.exists(thing):
				info["path"]=thing
				info["mtime"]=getTime(thing)
				info["sha256"]=getHash(thing)
				with open(thing,"rb") as fd:
					info["sample"]=fd.read()[:100]
				malware.append(info)
			else:
				print("{}[{}!{}] {} does not exist or inaccessible{}".format(WHITE,RED,WHITE,thing,CLR))
				log(thing,"does not exist or inaccessible.",False)
				pass
		if sendMe(malware):
			print("{}[{}+{}] Email sent successfully: {}{}{}".format(WHITE,GRN,WHITE,BLU,", ".join([str(f["path"]) for f in malware]),CLR))
		else: print("{}[{}!{}] Email not sent: {}{}{}".format(WHITE,RED,WHITE,BLU,", ".join([str(f["path"]) for f in malware]),CLR))
	except KeyboardInterrupt:
		print("[")
		exit(1)
	except Exception as err: print("Error: {}".format(err))

if __name__=="__main__":
	main()
