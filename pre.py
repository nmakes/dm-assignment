import csv

# Enter file name here
file_name = '../Dataset/decSales.csv'

output = []

with open(file_name, 'rb') as csv_file:

    reader = csv.reader(csv_file, delimiter=',')

    next(reader)

    support_count = {}
    support_count_ant = {}
    price_dict = {}

    for i in reader:

        itemID = i[1]
        date_time = i[3]
        date = date_time.split(' ')[0]
        time = date_time.split(' ')[1]
        studID = i[-3]


# P1.readNewPrices()
# P1.calculateProfitAndPenalty()

output.append([itemID, date, time, studID])

output.sort(key=lambda x: x[2])
output.sort(key=lambda x: x[-1])
output.sort(key=lambda x: x[1])


with open('decMod.csv', 'wb') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    for o in output:

        print o
        writer.writerow(o)
