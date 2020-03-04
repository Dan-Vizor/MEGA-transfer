#!/usr/bin/python3 
__version__ = 0.1
import json, os, random

def error(ErrorMessage):
	print("Error: " + ErrorMessage)
	raise SystemExit

def ReadJSON(File):
	try:
		# from https://stackoverflow.com/questions/20199126/reading-json-from-a-file
		with open(File) as f:
			return json.load(f)
	except IOError:
		error("unable to locate file ({})".format(File))

print("This is a alpha version of MEGA transfer.\nPlease report bugs to the developer.\n") # alpha software disclamer

SelectedFilesDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "selected files/")
if not os.path.exists(SelectedFilesDir): os.makedirs(SelectedFilesDir)


while True:
	x = input("Download .json files from MEGA, move them into the 'sellected files' folder and press enter to genorate request file.\n")
	if x.lower().rstrip() == "shutdown":
		# make shutdown request file
		print("made shutdown request")
		raise SystemExit

	files = [ f for f in os.listdir(SelectedFilesDir) if os.path.isfile(os.path.join(SelectedFilesDir,f)) ] # get list of files

	if files == []:
		print("Error: no files found\n")
		continue

	x = input("confirm request of {} file(s) (Y/n) ".format(len(files)))
	if x.lower().rstrip() == "y":
		# make requset .json file
		ContentList = []
		TotalSize = 0
		for file in files:
			each = ReadJSON(SelectedFilesDir + file)
			ContentList += [each]
			TotalSize += each["size"]
		#print(ContentList)

		OutFileName = "request "
		for i in range(20):
			OutFileName += str(random.randint(0, 10))
		OutFileName += ".json"

		# write to file
		doc = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), OutFileName), "w")
		json.dump({"files": ContentList, }, doc)
		doc.close()

		print("genorated: {} with a total size of {} bytes".format(OutFileName, TotalSize))
		break
	else:
		print("\n")
		continue