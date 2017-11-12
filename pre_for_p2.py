import csv

# Enter file name here
file_name = 'Dataset/augSales.csv'

file_output = {}

output = []

with open(file_name, 'rb') as csv_file:

    reader = csv.reader(csv_file, delimiter=',')

    next(reader)

    support_count = {}
    support_count_ant = {}
    price_dict = {}

    for i in reader:

        billNo = i[0]
        itemID = i[1]
        date = i[3]
        date = date.split(' ')[0]

        if (date, billNo) in file_output:

            file_output[(date, billNo)].append(itemID)

        else:
            file_output[(date, billNo)] = [itemID]

with open('p2data.csv', 'wb') as csvfile:

    writer = csv.writer(csvfile, delimiter=',')

    for i in file_output:

        writer.writerow([i[0], i[1], file_output[i]])

        print[i[0], i[1], file_output[i]]
