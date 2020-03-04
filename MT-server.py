#!/usr/bin/python3 
__version__ = 0.1
import json, os, time

def log(message):
	LogFile = "log.txt"
	doc = open(LogFile, "a")
	LocalTime = time.localtime()
	timestamp = "{}:{}:{}".format(LocalTime.tm_hour, LocalTime.tm_min, LocalTime.tm_sec)
	date = "{}/{}/{}".format(LocalTime.tm_mday, LocalTime.tm_mon, LocalTime.tm_year)

	doc.write("[{} {}] {}\n".format(date, timestamp, message))
	doc.close()

def error(ErrorMessage):
	log("Error: " + ErrorMessage + "\n")
	print("Error: " + ErrorMessage)
	#raise SystemExit

def ReadJSON(File):
	try:
		# from https://stackoverflow.com/questions/20199126/reading-json-from-a-file
		with open(File) as f:
			return json.load(f)
	except IOError:
		error("unable to locate file ({})".format(File))

# start up
#UserArgs = sys.argv[1:] # get command line arguments
SETTINGS = ReadJSON("settings.json")

RootDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "MEGA sync folder/")
if not os.path.exists(RootDir): os.makedirs(RootDir)

if not SETTINGS["ContentDir"].endswith("/"): ContentDir = SETTINGS["ContentDir"] + "/"
else: ContentDir = SETTINGS["ContentDir"]

# index folder structure
ArchiveDir = os.path.join(RootDir, "files/")
if not os.path.exists(ArchiveDir): os.makedirs(ArchiveDir)
dirs = [x[0] for x in os.walk(ContentDir)]
FilesCount = 0
for each in dirs:
	files = [ f for f in os.listdir(each) if os.path.isfile(os.path.join(each,f)) ] # get list of files in dir
	if files != []:
		NewDir = os.path.join(ArchiveDir, each.replace(ContentDir, ""))
		if not os.path.exists(NewDir): os.makedirs(NewDir)
		for file in files:
			content = {"name": file, "size": os.path.getsize(os.path.join(each, file)), "path": NewDir.replace(RootDir, "")}
			
			# change file extention to .json
			FileNameParts = file.split(".")
			del FileNameParts[-1]
			OutFileName = ""
			for part in FileNameParts: OutFileName += part + "."
			OutFileName += "json"

			# write to file
			doc = open(os.path.join(NewDir, OutFileName), "w")
			json.dump(content, doc)
			doc.close()
			FilesCount += 1

print("indexed {} files".format(FilesCount))

log("\n---server start---")
InputDir = os.path.join(RootDir, "input/")
if not os.path.exists(InputDir): os.makedirs(InputDir)
while True:
	# scan for new requests
	requests = [ f for f in os.listdir(InputDir) if os.path.isfile(os.path.join(InputDir,f)) ]
	print(requests)
	if requests != []:
		for request in requests:
			RequestContent = ReadJSON(request.rstrip())
			print(RequestContent)
			for each in RequestContent["files"]: print(each)
			exit()

			# perform checks
			# move chosen files to output dir

	time.sleep(SETTINGS["ScanInterval"])