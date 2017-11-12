import csv
import config
from sys import stdout
from itertools import combinations as nCr
import time


start_time = time.time()


monthFile = open("p2/novFinal.csv")
monthWisePricelistFile = open("Dataset/monthwisePriceList.csv")
reader = csv.reader(monthFile, delimiter=',')

support_count = {}

minsup = 0.000001
minconf = 0.000001

ItemSetSize = 3
AnticedentSize = 2

displayLiveResult = False

def removeDups(li):
	
	for i in range(len(li)):
		li[i] = frozenset(li[i])

	return li

def extractData(reader):
	retList = []

	for line in reader:
		
		l = eval(line[1])
		intL = []

		for itemID in l:
			intL.append(int(itemID))

		retList.append(intL)

	removeDups(retList)

	return retList

def itemSubsetSupportCount(data, itemSubset):

	support_count = 0

	for itemset in data:
		if itemSubset.issubset(itemset):
			support_count += 1

	return support_count


def loadItems(monthWisePricelistFile):
	reader = csv.reader(monthWisePricelistFile, delimiter=',')

	reader.next()
	items = {}

	for l in reader:
		items[int(l[0])] = l[1]

	return items


def nItemSubsetSupportCount(data, items, n, limit = None): # limit limits the number of iterations

	support_count = {}
	net_support_count = 0

	subsets = frozenset(nCr(items, n))

	if limit == None:
		limit = len(subsets)

	for subset in subsets:

		key = frozenset(subset)
		sc = 0

		for itemset in data:
			if key.issubset(itemset):
				sc += 1

		if sc!=0:

			if key in support_count:
				print "!!FATAL ERROR!!: RECURRING ITEMSET. CHECK CODE AGAIN"
			else:
				support_count[key] = sc
				net_support_count += sc

		limit -= 1

		if limit==0:
			break

	return support_count, net_support_count


def getSupportFromCount(support_count, net_support_count, minsup=0):

	support = {}

	for i in support_count:
		sup = float(support_count[i] / float(net_support_count))
		
		if sup > minsup:
			support[i] = sup

	return support


def getBestAssociation(supports, ant_supports):

	bestAssociations = []

	ant_length = len(ant_supports.keys()[0])

	for itemset in supports:

		ant_combos = list(nCr(itemset, ant_length))
		ants = []
		
		for c in ant_combos:
			ants.append(frozenset(c))

		ants = frozenset(ants)

		#print ants

		minAnt = None
		minAntSup = 1

		for ant in ants:
			# the anticedent with the lower support count would yield a higher confidence of the association rule

			if ant in ant_supports.keys():
			
				if minAnt == None:
					minAnt = ant
					minAntSup = ant_supports[minAnt]
				else:
					if ant_supports[ant] < minAntSup :
						minAnt = ant
						minAntSup = ant_supports[minAnt]

		if minAnt != None:

			consequent = itemset.difference(frozenset(minAnt))
			bestConf = float(supports[itemset] / minAntSup)

			bestAssociations.append( (minAnt, consequent, bestConf ) )

	return bestAssociations

items = loadItems(monthWisePricelistFile)
# print items

print
print "EXTRACTING DATA ...",

data = extractData(reader)

print "... complete",
print "--- %s seconds ---" % (time.time() - start_time)
if displayLiveResult: stdout.flush()

print
print "minsup =", minsup
print "minconf =", minconf
print "associations : ", AnticedentSize, "-->", ItemSetSize - AnticedentSize
print
if displayLiveResult: stdout.flush()


print 
print "FINDING ITEMSET SUPPORT",
if displayLiveResult: stdout.flush()

supports, net_support_count = nItemSubsetSupportCount(data, items, ItemSetSize)
supports = getSupportFromCount(supports, net_support_count, minsup)

print "... complete",
print "--- %s seconds ---" % (time.time() - start_time)
if displayLiveResult: stdout.flush()

print
print "FINDING SUBSET SUPPORT",
if displayLiveResult: stdout.flush()

ant_supports, ant_net_support_count = nItemSubsetSupportCount(data, items, AnticedentSize)
ant_supports = getSupportFromCount(ant_supports, ant_net_support_count, minsup)

print "... complete",
print "--- %s seconds ---" % (time.time() - start_time)
print
if displayLiveResult: stdout.flush()


print "ITEMSETS WITH SUPPORT > MINSUP AS FOLLOWS:-"
print
if displayLiveResult: stdout.flush()

for i in sorted(supports):
	if supports[i] > minsup:
		itemNames = [items[x] for x in i]
		print i, "|", itemNames, " : ", supports[i]
		if displayLiveResult: stdout.flush()

print
print "GETTING BEST ASSOCIATIONS",
if displayLiveResult: stdout.flush()

bestAssociations = getBestAssociation(supports, ant_supports)

print "... complete",
print "--- %s seconds ---" % (time.time() - start_time)
print
if displayLiveResult: stdout.flush()


for i in bestAssociations:
	ant = i[0]
	con = i[1]
	conf = i[2]

	if conf > minconf:
		antItemNames = [items[x] for x in ant]
		conItemNames = [items[x] for x in con]

		print antItemNames, "-->", conItemNames, " : ", conf
		if displayLiveResult: stdout.flush()

print
print "COMPLETED"
print "total execution time =", "--- %s seconds ---" % (time.time() - start_time)