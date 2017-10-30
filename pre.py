'''

Preprocessing the data for ARM:

1. Finding the hour number (As an hour number where 1 is 4 pm)
2. Finding the student's group (First year, second year, etc)

'''

import csv

slots = { "16":1, "17":2, "18":3, "19":4, "20":5, "21":6, "22":7, "23":8, "0":9, "1":10, "2":11}
slots2 = { "16":"4:30 PM", "17":"5:30 PM", "18":"6:30 PM", "19":"7:30 PM", "20":"8:30 PM", "21":"9:30 PM", "22":"10:30 PM", "23":"11:30 PM", "00":"12:30 AM", "01":"1:30 AM"}
slots3 = { "16":"4-5 PM", "17":"5-6 PM", "18":"6-7 PM", "19":"7-8 PM", "20":"8-9 PM", "21":"9-10 PM", "22":"10-11 PM", "23":"11-12 AM", "00":"12-1 AM", "01":"1-2 AM"}

INF = 100
ZERO = 0

minsup = 0.4
minconf = ZERO
maxsup = INF
maxconf = INF

def getTimeSlot(absHour):

    # return slots2[str(absHour)]
    return slots3[str(absHour)]

def runFuncOnFiles(monthFileList, monthWisePricelistFile, monthFileNameList = None):

    print "ASSOCIATION RULES"
    print "student_gp , time_slot -> item"

    print
    print "minsup: ", minsup, "%"
    print "minconf: ", minconf, "%"
    print "maxsup: ", maxsup, "%"
    print "maxconf: ", maxconf, "%"
    print

    for i in range(len(monthFileList)):
        print "Running on file: ", monthFileNameList[i]
        print
        monthWisePricelistFile.seek(0,0)
        myFunc(monthFileList[i], monthWisePricelistFile)
        print "--x--x--"
        print


def myFunc(monthFile, monthWisePricelistFile):

    file_output = []

    reader = csv.reader(monthFile, delimiter=',')

    next(reader)

    # for i in reader:

    #     string = i[3][11:]
    #     comp = string.rsplit(':')

    #     student_group = i[5][:2]

    #     file_output.append([int(i[1]), int(i[2]), int(comp[0]), float(i[4]),
    #                         student_group, int(i[6]), int(i[7])])

    support_count = {}
    support_count_ant = {}
    price_dict = {}

    total_entries = 0

    for i in reader:
        itemID = i[1]
        absHour = (((i[3].split())[1]).split(':'))[0]
        group = i[5][0:2]
        price = i[4]

        total_entries += 1

        price_dict[itemID] = price

        if((group, absHour, itemID) in support_count.keys()):
            support_count[(group, absHour, itemID)] += 1
            if int(itemID) > 1400:
                print i
        else:
            support_count[(group, absHour, itemID)] = 1

        if (group, absHour) in support_count_ant.keys():
            support_count_ant[(group, absHour)] += 1
        else:
            support_count_ant[(group, absHour)] = 1

    priceListReader = csv.reader(monthWisePricelistFile, delimiter=',')
    next(priceListReader)

    items = {}

    for i in priceListReader:
        items[i[0]] = i[1]

    outputCount = 0

    for keys in support_count.keys():
        
        (group, absHour, itemID) = keys
        sup = float(support_count[keys]) * 100 / float(total_entries)
        conf = float( float(support_count[keys]) * 100 / float(support_count_ant[(group, absHour)]))

        if ( sup > minsup ) and ( sup < maxsup ) and ( conf > minconf ) and ( conf < maxconf ):
            outputCount += 1
            print group, ",", getTimeSlot(absHour), " -> ", items[itemID],
            print " : s=", str(sup), "% | c=", conf, "%"

    print "\n Total outputCount: ", outputCount


monthFileList = [open('Dataset/augSales.csv'), open('Dataset/sepSales.csv'), open('Dataset/octSales.csv'), open('Dataset/novSales.csv')]
monthFileNameList = ['Dataset/augSales.csv', 'Dataset/sepSales.csv', 'Dataset/octSales.csv', 'Dataset/novSales.csv']
monthWisePricelistFile = open('Dataset/monthwisePriceList.csv')

runFuncOnFiles(monthFileList, monthWisePricelistFile, monthFileNameList)

# with open('pre_data.csv', 'w', newline='') as csvfile:

#     writer = csv.writer(csvfile, delimiter=',')

#     for i in file_output:
#         writer.writerow(i)
