class Problem1:

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
		pass

	@staticmethod
	def penalty(newPriceList, oldPriceList, hoursList, segmentList):

		totalPenalty = 0

		if len(newPriceList) == len(oldPriceList) == len(hourList) == len(segmentWeightList):
			for i in range(newPriceList):
				totalPenalty += ( (newPriceList[i] - oldPriceList[i]) * Problam1.getHourWeight(hourList[i]) * Problem1.getSegmentWeight(segmentWeightList[i]) )

		return totalPenalty