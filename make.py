#!/usr/bin/env python3
import os,sys
try:
	import hugg, requests
except:
	os.system("{0} -m pip install --upgrade pip hugg requests".format(sys.executable))
	import hugg, requests

def run(string):
	print(string)
	os.system(string)

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Semgrep Rules Archiving")
	parser.add_argument("-t","--token", help="The user github token",nargs=1, default=None)
	parser.add_argument("-j","--java", action="store_true",default=False, help="Pull the Java Files")
	parser.add_argument("-p","--python", action="store_true",default=False, help="Pull the Python Files")
	parser.add_argument("-s","--save", action="store_true",default=False, help="Request a save of the repo within the webarchive")
	return parser.parse_args()

if __name__ == '__main__':
	args = getArgs()
	expression = None

	if args.java and args.python:
		expression = lambda x:x.startswith("generic") or x.startswith("java/") or x.startswith("python/")
	elif args.java:
		expression = lambda x:x.startswith("generic") or x.startswith("java/")
	elif args.python:
		expression = lambda x:x.startswith("generic") or x.startswith("python/")

	if args.save:
		url = "https://codeload.github.com/returntocorp/semgrep-rules/zip/refs/heads/develop"
		requests.post("https://web.archive.org/save/"+str(url), {
			"url":url,
			"capture_outlinks":"1",
			"capture_all":"on",
			"capture_screenshot":"on"
		})

	if expression != None:
		repo = hugg.ghub("returntocorp/semgrep-rules",str(args.token[0]))
		for foil in repo.files():
			if expression(foil):
				print(foil)
				path = os.path.abspath(foil).replace(os.path.basename(foil),'')
				run("mkdir -p {0}".format(path))
				repo.download(foil, foil)
