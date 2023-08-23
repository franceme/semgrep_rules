#!/usr/bin/env python3
import os,sys
try:
    import hugg
except:
    os.system("{0} -m pip install --upgrade pip hugg".format(sys.executable))
    import hugg

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Semgrep Rules Archiving")
	parser.add_argument("-j","--java", action="store_true",default=False, help="Pull the Java Files")
	parser.add_argument("-p","--python", action="store_true",default=False, help="Pull the Python Files")
	return parser.parse_args()

if __name__ == '__main__':
	args = getArgs()
    expression = None

    if args.java and args.python:
        expression = lambda x:x.startswith("java") or x.startswith("python")
    elif args.java:
        expression = lambda x:x.startswith("java")
    elif args.python:
        expression = lambda x:x.startswith("java")

    if expression != None:
        repo = hugg.ghub("returntocorp/semgrep-rules")
        for foil in repo.files():
            if expression(foil):
                repo.download(foil, foil)
