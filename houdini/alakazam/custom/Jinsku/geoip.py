#!/usr/bin/python
# A tool for gathering basic info
# Created by Jinsku, free for anyone to use (https://github.com/jinsku)
# Requires a Shodan API key (https://shodan.io)
import sys,json,re,socket
if sys.version_info >= (3,0):
	version=3
	import urllib.request
else:
	version=2
	import urllib2 as urllib

API=""
if not API: print("API Key required");exit(1)

def main():
	try: search=sys.argv[1]
	except: print("Argument required"); exit(1)
	if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",search):
		try: search=socket.gethostbyname(search)
		except Exception as err: print("Error: "+str(err));exit(1)
	if version==2:
		try:
			response=urllib.urlopen("https://api.shodan.io/shodan/host/{0}?key={1}".format(search, API))
			response=json.load(response)
		except Exception as err: print("Error: "+str(err));exit(1)
	elif version==3:
		print("Python3 not yet supported, sorry :(")
		exit(1)
	"""
	TODO: Find a way to make Py3 work with the bytestring returned by urllib (06/01)
		try:
			response=urllib.request.urlopen("https://api.shodan.io/shodan/host/{0}?key={1}".format(search, API))
			response=response.read()
			decode=json.JSONDecoder().decode()
			response=decode(response)
		except Exception as err: print("Error: "+str(err));exit(1)
	"""
	try: print(response["ip_str"]+" -"),
	except Exception as err: print("IP Error: "+str(err))
	try: print(response["country_code"]+" -"),
	except Exception as err: print("Country Error: "+str(err))
	try: print(response["region_code"])
	except Exception as err: print("Region Error: "+str(err))
	try: print("Hostname: "+response["hostnames"][0])
	except Exception as err: print("Hostname Error: "+str(err))
	try: print("Company: "+response["isp"])
	except Exception as err: print("Owner Error: "+str(err))
	try: print("Ports: "+str(response["ports"])[1:-1])
	except Exception as err: print("Ports Error: "+str(err))

if __name__=="__main__":
	main()
