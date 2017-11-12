import csv
import config

class P1:

	@staticmethod
	def getTimeSlot(absHour):

		# return slots2[str(absHour)]
		return config.slots3[str(absHour)]


	@staticmethod
	def getSegmentWeight(segment):

		if segment=='F1':
			return 12
		elif segment=='F2':
			return 32
		elif segment=='F3':
			return 30
		elif segment=='F4':
			return 20
		elif segment=='F5':
			return 3
		elif segment=='H1':
			return 2
		elif segment=='H1':
			return 2
		else:
			return 1


	@staticmethod
	def getHourWeight(hours):
		if hours > 6:
			return 6**2
		else:
			return (hours ** 2)


	@staticmethod
	def getSegmentWeight(segment):
		if segment=='F1':
			return 12
		elif segment=='F2':
			return 32
		elif segment=='F3':
			return 30
		elif segment=='F4':
			return 20
		elif segment=='F5':
			return 3
		elif segment=='H1':
			return 2
		elif segment=='H2':
			return 2
		else:
			return 1


	@staticmethod
	def penalty(newPriceList, oldPriceList, hoursList, segmentList):

		totalPenalty = 0

		if len(newPriceList) == len(oldPriceList) == len(hourList) == len(segmentList):
			for i in range(newPriceList):
				totalPenalty += ( (newPriceList[i] - oldPriceList[i]) * P1.getHourWeight(hourList[i]) * P1.getSegmentWeight(segmentList[i]) )

		return totalPenalty
	

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
			P1.Func1(monthFileList[i], monthWisePricelistFile)
			print "--x--x--"
			print
	

	@staticmethod
	def Func1(monthFile, monthWisePricelistFile):	
		'''
			Obtain associations of the form:

				student_gp , time_slot -> item

			where,
			student_gp: student group (or segment)
			time_slot: hour in which the purchase is made
			item: the item that was purchased
		'''

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

			if ( sup > config.minsup ) and ( sup < config.maxsup ) and ( conf > config.minconf ) and ( conf < config.maxconf ):
				outputCount += 1
				print group, ",", P1.getTimeSlot(absHour), " -> ", items[itemID],
				print " : s=", str(sup), "% | c=", conf, "%"

		print "\n Total outputCount: ", outputCount



# CALCULATING PROFIT

	@staticmethod
	def readNewPrices():
		
		newPrices = {}
		segments = ['F1','F2','F3','F4','F5','H1','H2','oth']
		i = 0

		with open(config.newPriceFileName) as newPriceFile:
			
			newPriceReader = csv.reader(newPriceFile, delimiter=',')
			headRead = True

			i = 0

			for line in newPriceReader:
				
				if headRead:
					header = line
					# print header
					headRead = False
				else:
					itemID = line[0]
					hour = line[2]
					price = line[1]

					newPrices[ (itemID, hour) ] = {}
					i = 3
					
					for segment in segments:
						newPrices[ (itemID, hour) ][segment] = line[i]
						i += 1

			# print newPrices.keys()

		return newPrices


	@staticmethod
	def calculateProfit():

		'''
			decemberData[itemID] = qty
			where qty is the quantity of item <itemID> sold in december
		'''
		decemberData = {}
		totalItemsSold = 0
		profit = 0

		with open(config.decemberFileName) as decemberFile:

			decReader = csv.reader(decemberFile)
			
			ignoreHead = True

			for line in decReader:

				if ignoreHead:
					ignoreHead = False
				else:

					# print line
					itemID = int(line[2])
					qty = int(line[3])

					# print itemID, qty

					if itemID in decemberData.keys():
						decemberData[itemID] += qty
						totalItemsSold += qty
					else:
						decemberData[itemID] = qty
						totalItemsSold += qty

		dat = [(key, decemberData[key]) for key in sorted(decemberData.keys())]
		print dat
		print len(dat)
		print totalItemsSold


		newPrices = P1.readNewPrices()
		profit = 0
		
		for (itemID, hour) in newPrices.keys():
			