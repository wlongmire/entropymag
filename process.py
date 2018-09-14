import csv

cvs_entries = open('entries.csv')
reader = csv.DictReader(cvs_entries)

dict_entries = []
for row in reader:
    dict_entries.append(row)

print dict_entries