import requests as re
import json
import sys

##################### SCHEDGE DATA DOWNLOADER #####################

ROOT_URL = "https://schedge.a1liu.com/"
SUBJECT_URL = ROOT_URL + "subjects"
sems = ["fa", "su", "sp", "ja"]
res = re.get(SUBJECT_URL)
contents = json.loads(res.content)
data = []

sem = sys.argv[1]
year = sys.argv[2]
full = False
if len(sys.argv) == 4:
    full = True
if sem not in sems:
    raise ValueError("Invalid semester " + sem)

# @ToDo handle error
for subject in contents:
    for subjectCode in contents[subject]:
        print("Retrieving course data for " + subjectCode + "-" + subject)
        result = re.get(ROOT_URL + year + "/" + sem + "/" + subject + "/" + subjectCode)
        if full:
            result = re.get(ROOT_URL + year + "/" + sem + "/" + subject + "/" + subjectCode + "?full=true")
        courses = json.loads(result.content)
        if not courses:
            print("No available data for " + subjectCode + "-" + subject)
        else:
            data += courses

file = None
if full:
    file = open("../data/" + year + sem + "full.json", "w")
else:
    file = open("../data/" + year + sem + ".json", "w")
with file as f:
    for course in data:
        course = json.dumps(course)
        f.write("%s\n" % course)

if file: file.close()


