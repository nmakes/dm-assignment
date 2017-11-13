import csv
from sys import stdout
from itertools import combinations as nCr
import time

start_time = time.time()
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

    next(reader)
    items = {}

    for l in reader:
        items[int(l[0])] = l[1]

    return items


def nItemSubsetSupportCount(data, items, n, limit=None):

    # limit limits the number of iterations

    support_count = {}
    net_support_count = 0

    subsets = frozenset(nCr(items, n))

    if limit is None:
        limit = len(subsets)

    for subset in subsets:

        key = frozenset(subset)
        sc = 0

        for itemset in data:
            if key.issubset(itemset):
                sc += 1

        if sc != 0:

            if key in support_count:
                print("!!FATAL ERROR!!: RECURRING ITEMSET. CHECK CODE AGAIN")
            else:
                support_count[key] = sc
                net_support_count += sc

        limit -= 1

        if limit == 0:
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

    ant_length = len(list(ant_supports.keys())[0])

    for itemset in supports:

        ant_combos = list(nCr(itemset, ant_length))
        ants = []

        for c in ant_combos:
            ants.append(frozenset(c))

        ants = frozenset(ants)
        print("----")
        print(itemset)
        print(ants)
        # print ants

        minAnt = None
        minAntSup = 1

        for ant in ants:
            # the anticedent with the lower support count would yield a higher
                        # confidence of the association rule

            if ant in list(ant_supports.keys()):

                print(ant)
                print(itemset)
                print

                if minAnt is None:
                    minAnt = ant
                    minAntSup = ant_supports[minAnt]
                else:
                    if ant_supports[ant] < minAntSup:
                        minAnt = ant
                        minAntSup = ant_supports[minAnt]

        if minAnt is not None:

            consequent = itemset.difference(frozenset(minAnt))
            bestConf = float(supports[itemset] / minAntSup)

            bestAssociations.append((minAnt, consequent, bestConf))

    return bestAssociations


def EXECUTEproblem2(mwplfile, monthFile, minsup, minconf, ItemSetSize,
                    AnticedentSize):

    reader = csv.reader(monthFile, delimiter=',')
    monthWisePricelistFile = open(mwplfile)
    items = loadItems(monthWisePricelistFile)
    # print items

    print()
    print("EXTRACTING DATA ...", end=' ')

    data = extractData(reader)

    print("... complete", end=' ')
    print("--- %s seconds ---" % (time.time() - start_time))
    if displayLiveResult:
        stdout.flush()

    print()
    print("minsup =", minsup)
    print("minconf =", minconf)
    print("associations : ", AnticedentSize, "-->",
          ItemSetSize - AnticedentSize)
    print()
    if displayLiveResult:
        stdout.flush()

    print()
    print("FINDING ITEMSET SUPPORT", end=' ')
    if displayLiveResult:
        stdout.flush()

    supports, net_support_count = nItemSubsetSupportCount(data, items,
                                                          ItemSetSize, 100)
    supports = getSupportFromCount(supports, net_support_count, minsup)

    print("... complete", end=' ')
    print("--- %s seconds ---" % (time.time() - start_time))
    if displayLiveResult:
        stdout.flush()

    print()
    print("FINDING SUBSET SUPPORT", end=' ')
    if displayLiveResult:
        stdout.flush()

    ant_supports, ant_net_support_count = nItemSubsetSupportCount(data, items, AnticedentSize, 100)
    ant_supports = getSupportFromCount(ant_supports, ant_net_support_count,
                                       minsup)

    print("... complete", end=' ')
    print("--- %s seconds ---" % (time.time() - start_time))
    print()
    if displayLiveResult:
        stdout.flush()

    print("ITEMSETS WITH SUPPORT > MINSUP AS FOLLOWS:-")
    print()
    if displayLiveResult:
        stdout.flush()

    for i in sorted(supports):
        if supports[i] > minsup:
            itemNames = [items[x] for x in i]
            print(i, "|", itemNames, " : s=", supports[i])
            if displayLiveResult:
                stdout.flush()

    print()
    print("GETTING BEST ASSOCIATIONS", end=' ')
    if displayLiveResult:
        stdout.flush()

    bestAssociations = getBestAssociation(supports, ant_supports)

    print("... complete", end=' ')
    print("--- %s seconds ---" % (time.time() - start_time))
    print()
    if displayLiveResult:
        stdout.flush()

    for i in bestAssociations:
        ant = i[0]
        con = i[1]
        conf = i[2]

        if conf > minconf:
            antItemNames = [items[x] for x in ant]
            conItemNames = [items[x] for x in con]

            print(antItemNames, "-->", conItemNames, " : c=", conf)
            if displayLiveResult:
                stdout.flush()

    print()
    print("COMPLETED")
    print("total execution time =", "--- %s seconds ---" % (time.time() - start_time))


def loadRatings():
    months = ["Dataset/augSales", "Dataset/sepSales", "Dataset/octSales",
              "Dataset/novSales"]

	for m in months:
		ratings = {}
		monthFile = open(m)
		reader = csv.reader(monthFile, delimiter=',')
		for line in reader:
			Id = line[1]
			Rating = line[7]

			if Id in ratings:

# _____________________________________________________________________________


monthFiles = ["p2/novFinal.csv", ]

''' ["p2/novFinal.csv", "p2/octFinal.csv", "p2/sepFinal.csv",
              "p2/augFinal.csv"] '''

mwplfile = "Dataset/monthwisePriceList.csv"

minsup = 0.00001
minconf = 0.01

ItemSetSizes = [2, ]  # 3, 4]
AnticedentSizes = [1, ]  # 2, 3]

for mf in monthFiles:

    for i in range(len(ItemSetSizes)):

        ItemSetSize = ItemSetSizes[i]
        AnticedentSize = AnticedentSizes[i]
        monthFile = open(mf)

        print()
        print("==================================================")
        print("monthFile: ", monthFile)
        print("minsup: ", minsup)
        print("minconf: ", minconf)
        print("ItemSetSize: ", ItemSetSize)
        print("AnticedentSize: ", AnticedentSize)
        print("==================================================")
        print()

        EXECUTEproblem2(mwplfile, monthFile, minsup, minconf,
                        ItemSetSize, AnticedentSize)
