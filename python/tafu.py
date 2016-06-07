#!/bin/python3
# The Amazing F U, an active GEO IP-based blacklisting utility
# Created by Jinsku, free for anyone to use (https://github.com/jinsku)
# Freegeoip.net offers 10,000 requests per hour for free
import sys,json,os,subprocess,datetime,time
from daemonize import Daemonize

def request(check):
	# Gather IP and country code
	response=None
	try: 
		if sys.version_info >= (3,0):
			import urllib
			response=urllib.request.urlopen("https://freegeoip.net/json/{0}".format(check))
		else: 
			import urllib2
			response=urllib2.urlopen("https://freegeoip.net/json/{0}".format(check))
		response=json.loads(response.read())
	except: pass
	return response

def log(ip,**kwargs):
	# Log IPs that are blocked
	present=datetime.datetime.now()
	with open("/var/log/tafu.log","a+") as f:
		f.write("{0} - {1} blocked\n".format(present,ip))

def readns():
	# Parse netstat and find instances of offending IPs, reutnr slist of block_ips
	# Possible solutions:
	# netstat -pant |grep ESTABLISHED | awk '{ print $5 }' | cut -d: -f1 | sort -u
	# ss -pant |grep ESTAB | awk '{ print $5 }' | cut -d: -f1 | sort -u
	# psutil module: https://pypi.python.org/pypi/psutil
	try: import psutil
	except: print("Requires psutil")
	ips=[ips[4] for ips in psutil.net_connections()]
	ips=set([ip for ip in ips if ip])
	return ips

def already_blocked(ip):
	if ip in str(subprocess.Popen("ip r",shell=True)): return True
	else: return False

def block(ip):
	# Block IP
	try: 
		blocked=subprocess.Popen("ip r add blackhole {0}".format(ip),shell=True)
		return blocked
	except Exception as err: return "Error: "+str(err)

def daemon():
	# Daemonize this bitch
	pid="/tmp/tafu.pid"
	try: from daemonize import Daemonize
	except: print("Requires Daemonize")
	daemon=Daemonize(app="tafu",pid=pid,action=main)
	daemon.start()

def main():
	# Adjust blacklist, whitelist, and log file location as necessary
	# Blacklist uses country codes, but you can change request(ip)["country_code"] below
	blacklist=["ca","za"]
	whitelist=["216.158.224.59","127.0.0.1","66.68.51.182","173.193.145.132"]
	while True:
		for ip in readns():
			ip=ip[0]
			if ip not in whitelist:
				print(ip)
				if already_blocked(ip) is False:
					try: 
						country=request(ip)["country_code"].lower()
						time.sleep(3)
						if country in blacklist:
							try: blocked=block(ip)
							except Exception as err: log(ip,err=err)
							if blocked:
								log(ip)
					except: pass

if __name__=="__main__":
#	try: daemon()
#	except OSError as err: print("Error: "+str(err));exit(0)
	main()
