#!/usr/bin/python
# A tool for doing stuff and also things
# Created by Jinsku, free for anyone to use (https://github.com/jinsku)
# Requires a Shodan API key (https://shodan.io) and Shodan Python module
import shodan,sys,optparse
KEY="8VEIOxLLP7qETm6h9dGCMXVS58tBRXEk"
api=shodan.Shodan(KEY)

def options():
	# Parse your options
	parser=optparse.OptionParser(usage="usage: %prog [options] <argument>",
								version="%prog 0.1")
	parser.add_option("-v","--verbose",
					action="store_true",default=False,
					dest="verbose",
					help="returns verbose results")
	opts,args=parser.parse_args()
	if len(args)<1:
		print("Error: No Argument Provided\n")
		parser.print_help()
		exit(1)
	return opts,args


def main():
	opts,args=options()
	check=args[0]
	if opts.verbose:
		pass
	else:
		try:
			results=api.search(check)
			print('{0} results found: {1}'.format(check,results['total']))
		except shodan.APIError, e:
			print("Error: {0}".format(e))

if __name__=="__main__":
	main()
