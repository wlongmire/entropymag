import csv
import pprint
import unicodedata

def processBodyEntry(entry):
    return entry.strip().decode('ascii', 'ignore').encode("utf-8")

def filterEntry(entry):
    return entry != ''

cvs_entries = open('entries_clean.csv')
reader = csv.DictReader(cvs_entries)

dict_entries = []
for row in reader:
    bodyEntry = filter(
        filterEntry,
        map(
            processBodyEntry,
            row['body'].split('/ ')
        )
    )
    dict_entries.append(bodyEntry)

pprint.pprint(dict_entries)