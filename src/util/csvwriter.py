import csv

def csvwriter(filename):
    csvfile = file(filename, 'wb')
    writer = csv.writer(csvfile,dialect='excel',delimiter=";")
    return csvfile,writer