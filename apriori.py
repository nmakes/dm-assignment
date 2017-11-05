class Apriori:
	
	def __init__(self, records = []):

		self.support_count = {}
		self.support_count_ant = {}
		self.price_dict = {}
		self.total_entries = len(records)
		self.records = records

	def scanFile(file):

		records = {}
		reader = csv.reader(file, delimiter=',')
		readHeader = True

		sno = 0
		header = []

		for line in reader:
			if readHeader:
				header = line
			else:
				sno += 1
				records[sno] = {}
				for i in range(len(line)):
					records[sno][header[i]] = line[i]

	