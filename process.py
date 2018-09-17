import re
from datetime import date
from datetime import datetime
import csv
import pprint


entry = [
    'Open: December 30, 2018',
    'Poetry, Fiction, Nonfiction, Art',
    '$3'
]

conversions = [
    {
        'type': 'Deadline',
        'entryIndex': 0,
        'regEx': [
            {
                'reg': r"^Deadline: (?P<open>.*) - (?P<deadline>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Deadline: (?P<open>.*) - (?P<deadline>.*$)", entry, flags=re.IGNORECASE).group('deadline'), '%B %d, %Y').date()
            },
            {
                'reg': r"^Deadline: (?P<deadline>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Deadline: (?P<deadline>.*$)", entry, flags=re.IGNORECASE).group('deadline'), '%B %d, %Y').date()
            }
        ]
    },
    {
        'type': 'Opens',
        'entryIndex': 0,
        'regEx': [
            {
                'reg': r"^Deadline: (?P<open>.*) - (?P<deadline>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Deadline: (?P<open>.*) - (?P<deadline>.*$)", entry, flags=re.IGNORECASE).group('open'), '%B %d, %Y').date()
            },
            {
                'reg': r"^Open: (?P<open>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Open: (?P<open>.*$)", entry, flags=re.IGNORECASE).group('open'), '%B %d, %Y').date()
            }
        ]
    }
]

currentConversion = conversions[1]
entrySearchIndex = currentConversion['entryIndex']
conversionRegex = currentConversion['regEx']
entry = entry[entrySearchIndex]

matches = filter(
    lambda regEntry : re.match(regEntry['reg'], entry, flags=re.IGNORECASE),
    conversionRegex
)

if len(matches) > 0:
    print matches[0]['result'](entry)
else:
    print None


#****************

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