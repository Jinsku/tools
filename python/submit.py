#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,hashlib,time,socket,smtplib,getpass,logging,binascii,pwd
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

def getHost():
	return socket.getfqdn(socket.gethostname())

def getSender():
	user=getpass.getuser()
	hostname=getHost()
	return user+"@"+hostname

def getUser(thing):
	uid=os.stat(thing).st_uid
	return pwd.getpwuid(uid).pw_name

def getSubmitter():
	return os.getlogin()

def sendMe(malware):
	hostname=getHost()
	if config["sender"] == None or config["sender"] == '':
		config["sender"]=getSender()
	subject="File report for {} - {}".format(hostname,getTime())
	header="From: {}\r\nTo: ".format(config["sender"])
	for user in config["to"]:
		header+="{},".format(user)
	header+="\r\nSubject: {}\r\n\r\n".format(subject)
	contents=header+"Greetings!\n\nOne or more files have been submitted for your review by {} on {} at {}.\n\n".format(getSubmitter(),hostname,getTime())
	for mal in malware:
		contents+="{:>16} {:>4}\n".format("======",mal["path"])
		contents+="{:>15}: {}\n".format("File",os.path.basename(mal["path"]))
		contents+="{:>15}: {}\n".format("Hostname",mal["host"])
		contents+="{:>15}: {}\n".format("Owner",mal["user"])
		contents+="{:>15}: {}\n".format("MTime",mal["mtime"])
		contents+="{:>15}: {}\n".format("MD5 Hash",mal["md5"])
		contents+="{:>15}: {}\n".format("SHA256 Hash",mal["sha256"])
		contents+="{:>15}: {}\n".format("Hex Signature",mal["sig"])
		contents+="{:>15}: {}\n\n".format("Sample",str(mal["sample"]))
	try:
		with smtplib.SMTP('localhost') as smtp:
			smtp.sendmail(config["sender"],config["to"],contents)	
			log(mal["path"],"submitted successfully.",True)
			return True
	except:
		log(mal["path"],"failed to submit.",False)
		return False

def getSig(md5):
	return binascii.hexlify(bytes(md5,"utf-8")).decode("utf-8")

def getHash(thing,sig):
	with open(thing,"r") as fd:
		if sig == "md5":
			response=hashlib.md5(fd.read().encode("utf-8")).hexdigest()
		elif sig == "sha256":
			response=hashlib.sha256(fd.read().encode("utf-8")).hexdigest()
	return str(response)

def getTime(thing=None):
	if thing:
		get=os.path.getmtime(thing)
		stime=time.strftime("%c",time.localtime(get))
	else:
		stime=time.strftime("%c",time.localtime())
	return stime

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
				info["user"]=getUser(thing)
				info["host"]=getHost()
				info["stime"]=getTime()
				info["mtime"]=getTime(thing)
				info["md5"]=getHash(thing,"md5")
				info["sha256"]=getHash(thing,"sha256")
				info["sig"]=getSig(info["md5"])
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
