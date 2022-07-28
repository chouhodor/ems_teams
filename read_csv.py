import csv

with open('pakar_csv.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)