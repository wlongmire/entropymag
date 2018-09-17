import re
from datetime import date
from datetime import datetime
import csv
import pprint
import unicodedata

# m = re.match(r"(?P<first>\w+) (?P<last>\w+)", "Malcolm Reynolds")

deadlineRE = [
    {
        'reg': r"^Deadline: (?P<deadline>.*$)",
        'result': lambda entry : datetime.strptime(re.match(r"^Deadline: (?P<deadline>.*$)", entry, flags=re.IGNORECASE).group('deadline'), '%B %d, %Y').date()
    },
    {
        'reg': r"^(?P<deadline>Now)",
        'result': lambda entry : date.today()
    },
    {
        'reg': r"^(?P<deadline>Year-Round)",
        'result': lambda entry : date.today()
    }
]

entry = "Year-Round" #"Deadline: November 1, 2018"# / Poetry / $30 / Prize: $3,000 + Publication,Presses"

deadlineMatches = filter(
    lambda regEntry :re.match(regEntry['reg'], entry, flags=re.IGNORECASE),
    deadlineRE)

if len(deadlineMatches) > 0:
    print deadlineMatches[0]['result'](entry)
else:
    print "Not Found"

# def processBodyEntry(entry):
#     return entry.strip().decode('ascii', 'ignore').encode("utf-8")

# def filterEntry(entry):
#     return entry != ''

# cvs_entries = open('entries_clean.csv')
# reader = csv.DictReader(cvs_entries)

# dict_entries = []
# for row in reader:
#     bodyEntry = filter(
#         filterEntry,
#         map(
#             processBodyEntry,
#             row['body'].split('/')
#         )
#     )
#     dict_entries.append(bodyEntry)

# pprint.pprint(dict_entries)