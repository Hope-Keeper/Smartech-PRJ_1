import csv

with open("loan.csv", "r") as f:
    lines = list(csv.reader(f))

print(lines)

del lines[1]

print(lines)