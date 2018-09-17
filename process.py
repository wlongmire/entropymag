import re
from datetime import date
from datetime import datetime
import csv
import pprint


# entries = [
#     [
#         'Open: December 30, 2018',
#         'Poetry, Fiction, Nonfiction, Art',
#         '$3'
#     ],
#     [
#         'Deadline: September 15, 2018',
#         'Poetry, Fiction, Nonfiction, Art',
#         '$3'
#     ],
#     [
#         'Deadline: August 22, 2018 - February 1, 2019',
#         'Poetry, Fiction, Nonfiction, Art',
#         '$3'
#     ],
#     [
#         'Now',
#         'Poetry, Fiction, Nonfiction, Art',
#         '$3'
#     ],
#     [
#         'Year-Round',
#         'Poetry, Fiction, Nonfiction, Art',
#         '$3'
#     ]
# ]

conversions = [
    {
        'type': 'deadline',
        'entryIndex': 0,
        'regEx': [
            {
                'reg': r"^Deadline: (?P<open>.*) - (?P<deadline>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Deadline: (?P<open>.*) - (?P<deadline>.*$)", entry, flags=re.IGNORECASE).group('deadline'), '%B %d %Y').date()
            },
            {
                'reg': r"^Deadline: (?P<deadline>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Deadline: (?P<deadline>.*$)", entry, flags=re.IGNORECASE).group('deadline'), '%B %d %Y').date()
            }
        ]
    },
    {
        'type': 'opens',
        'entryIndex': 0,
        'regEx': [
            {
                'reg': r"^Deadline: (?P<open>.*) - (?P<deadline>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Deadline: (?P<open>.*)( )- (?P<deadline>.*$)", entry, flags=re.IGNORECASE).group('open'), '%B %d %Y').date()
            },
            {
                'reg': r"^Open: (?P<open>.*$)",
                'result': lambda entry : datetime.strptime(re.match(r"^Open: (?P<open>.*$)", entry, flags=re.IGNORECASE).group('open'), '%B %d %Y').date()
            }
        ]
    }
]


# for any one entry, I want to loop over all conversions
def doConversion(conversion, entryArray):
    entrySearchIndex = conversion['entryIndex']
    conversionRegex = conversion['regEx']
    entry = entryArray[entrySearchIndex]

    matches = filter(
        lambda regEntry : re.match(regEntry['reg'], entry, flags=re.IGNORECASE),
        conversionRegex
    )

    if len(matches) > 0:
        #always takes the first match
        return { conversion['type']: matches[0]['result'](entry) }
    else:
        return { conversion['type']: None }

#****************

def processBodyEntry(entry):
    return entry.decode('ascii', 'ignore').encode("utf-8").strip()

def filterEntry(entry):
    return entry != ''

cvs_entries = open('entries_clean.csv')
reader = csv.DictReader(cvs_entries)

dict_entries = []
rows = []
for row in reader:
    bodyEntry = filter(
        filterEntry,
        map(
            processBodyEntry,
            row['body'].split('/')
        )
    )
    rows.append(row)
    dict_entries.append(bodyEntry)

for idx, entry in enumerate(dict_entries):
    entryObject = map(lambda conversion : doConversion(conversion, entry), conversions)
    # print entryObject
    print rows[idx]['org_name']