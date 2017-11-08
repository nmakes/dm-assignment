from problem1 import *
import config


'''

Preprocessing the data for ARM:

1. Finding the hour number (As an hour number where 1 is 4 pm)
2. Finding the student's group (First year, second year, etc)

'''

import csv

monthFileList = [open('Dataset/augSales.csv'), open('Dataset/sepSales.csv'), open('Dataset/octSales.csv'), open('Dataset/novSales.csv')]
monthFileNameList = ['Dataset/augSales.csv', 'Dataset/sepSales.csv', 'Dataset/octSales.csv', 'Dataset/novSales.csv']
monthWisePricelistFile = open('Dataset/monthwisePriceList.csv')

config.minsup = float(raw_input('Enter MinSup:'))
config.minconf = float(raw_input('Enter MinConf:'))

P1.runFunc1OnFiles(monthFileList, monthWisePricelistFile, monthFileNameList)

# -----------

with open("Dataset/newPrices.csv") as newPriceFile:

    newPriceReader = csv.reader(newPriceFile, delimiter=',')
    headRead = True

    for line in newPriceReader:
        
        if headRead:
            header = line
            print header
            headRead = False
        else:
            

# -----------