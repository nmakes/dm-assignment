import csv
import config

class P2:


	@staticmethod
	def runFunc1OnFiles(monthFileList, monthWisePricelistFile, monthFileNameList = None):

		print "ASSOCIATION RULES"
		print "student_gp , time_slot -> item"

		print
		print "minsup: ", config.minsup, "%"
		print "minconf: ", config.minconf, "%"
		print "maxsup: ", config.maxsup, "%"
		print "maxconf: ", config.maxconf, "%"
		print

		for i in range(len(monthFileList)):
			print "Running on file: ", monthFileNameList[i]
			print
			monthWisePricelistFile.seek(0,0)
			P2.Func1(monthFileList[i], monthWisePricelistFile)
			print "--x--x--"
			print


	@staticmethod
		def Func1(monthFile, monthWisePricelistFile):	
			'''
				Obtain associations between items:

					[item1 , item2 , ...] -> itemX

				where,
				the LHS contains 1 or more items, and RHS contains 1 item
				This association will find items bought together. This means, items that have been bought by a person, in a single bill.
			'''

			file_output = []

			reader = csv.reader(monthFile, delimiter=',')

			next(reader)

			support_count = {}
			support_count_ant = {}
			price_dict = {}

			total_entries = 0

			for i in reader:
				itemID = i[1]
				date = 

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

				if ( sup > config.minsup ) and ( sup < config.maxsup ) and ( conf > config.minconf ) and ( conf < config.maxconf ):
					outputCount += 1
					print group, ",", P1.getTimeSlot(absHour), " -> ", items[itemID],
					print " : s=", str(sup), "% | c=", conf, "%"

			print "\n Total outputCount: ", outputCount
