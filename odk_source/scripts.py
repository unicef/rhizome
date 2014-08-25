
import csv
with open ("/Users/johndingee_seed/Desktop/csv_exports/VCM_Summary.csv") as f:
    f_reader = csv.reader(f, delimiter = ',', quotechar="|")
    for row in f_reader:
        print ', '.join(row)
