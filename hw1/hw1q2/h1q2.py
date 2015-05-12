import operator

support = 100
# calculate frequent itemsets of size one
def oneitemset(filename):
	inputfile = open(filename, 'r')
	oneitemset = {}
	for line in inputfile:
		items = line.strip().split(' ')
		for itemid in items:
			if itemid in oneitemset:
				oneitemset[itemid] += 1
			else:
				oneitemset[itemid] = 1

	# delete all itemsets of size one which have less than 100 support
	for key, value in oneitemset.items():
		if value < support:
			del oneitemset[key]

	return oneitemset

# calculate frequent itemsets of size two
def twoitemset(oneitemset, filename):
	twoitemset = {}
	inputfile = open(filename, 'r')

	for line in inputfile:
		items = line.strip().split(' ')
		for item1 in items:
			for item2 in items:
				if items.index(item2) > items.index(item1):
					if item1 in oneitemset and item2 in oneitemset:
						# rearrange so that itemsets of size two is stored in alphabetical order
						if item1 < item2:
							item = item1 + "," + item2
						else:
							item = item2 + "," + item1
						if item in twoitemset:
							twoitemset[item] += 1
						else:
							twoitemset[item] = 1
							
	# delete all itemsets of size two which have less than 100 support
	for key, value in twoitemset.items():
		if value < support:
			del twoitemset[key]

	twoitemcf = {}
	for item in twoitemset:
			items = item.split(",")
			# calculate confidence of itemsets of size two
			twoitemcf[items[0] + " --> " + items[1]] = twoitemset[item] / float(oneitemset[items[0]])
			twoitemcf[items[1] + " --> " + items[0]] = twoitemset[item] / float(oneitemset[items[1]]) 

	# sort itemsets of size two based on value		   	
	sorted_twoitemcf = sorted(twoitemcf.items(), key = operator.itemgetter(1))
	
	# print top 5 rules with corresponding confidence scores in decreasing order of confidence score for itemsets of size two
	for i in range(1, 6):
		print sorted_twoitemcf[-i]

	return twoitemset

# helper function to sort itemsets of size three based in decreasing order of confidence score, then break the tie by lexicographically increasing order
def sortedhelper(item1, item2):
	if item1[1] > item2[1]:
		return 1
	elif item1[1] < item2[1]:
		return -1
	else:
		if item1[0] > item2[0]:
			return -1
		else:
			return 1

# calculate frequent itemsets of size three
def threeitemset(twoitemset, filename):
	inputfile = open(filename, 'r')
	threeitemset = {}

	for line in inputfile:
		items = line.strip().split(' ')
		for item1 in items:
			for item2 in items:
				for item3 in items:
					if items.index(item2) > items.index(item1) and items.index(item3) > items.index(item2):
						# rearrange so that itemsets of size three is stored in alphabetical order
						if item1 < item2 and item1 < item3 and item2 < item3:
							itemfirst = item1 + "," + item2
							itemsecond = item1 + "," + item3
							itemthird = item2 + "," + item3
							if itemfirst in twoitemset and itemsecond in twoitemset and itemthird in twoitemset:
								itemfinal = item1 + "," + item2 + "," + item3	
							else:
								continue				
						elif item1 < item2 and item1 < item3 and item2 > item3:
							itemfirst = item1 + "," + item3
							itemsecond = item1 + "," + item2
							itemthird = item3 + "," + item2
							if itemfirst in twoitemset and itemsecond in twoitemset and itemthird in twoitemset:
								itemfinal = item1 + "," + item3 + "," + item2
							else:
								continue
						elif item1 < item2 and item1 > item3:
							itemfirst = item3 + "," + item1
							itemsecond = item1 + "," + item2
							itemthird = item3 + "," + item2
							if itemfirst in twoitemset and itemsecond in twoitemset and itemthird in twoitemset:
								itemfinal = item3 + "," + item1 + "," + item2
							else:
								continue
						elif item1 > item2 and item1 < item3:
							itemfirst = item2 + "," + item1
							itemsecond = item2 + "," + item3
							itemthird = item1 + "," + item3
							if itemfirst in twoitemset and itemsecond in twoitemset and itemthird in twoitemset:
								itemfinal = item2 + "," + item1 + "," + item3
							else:
								continue
						elif item1 > item2 and item1 > item3 and item2 > item3:
							itemfirst = item3 + "," + item2
							itemsecond = item3 + "," + item1
							itemthird = item2 + "," + item1
							if itemfirst in twoitemset and itemsecond in twoitemset and itemthird in twoitemset:
								itemfinal = item3 + "," + item2 + "," + item1
							else:
								continue
						elif item1 > item2 and item1 > item3 and item2 < item3:
							itemfirst = item2 + "," + item3
							itemsecond = item2 + "," + item1
							itemthird = item3 + "," + item1
							if itemfirst in twoitemset and itemsecond in twoitemset and itemthird in twoitemset:
								itemfinal = item2 + "," + item3 + "," + item1
							else:
								continue
						if itemfinal in threeitemset:
							threeitemset[itemfinal] += 1
						else:
							threeitemset[itemfinal] = 1

	# delete all itemsets of size three which have less than 100 support
	for key, value in threeitemset.items():
		if value < support:
			del threeitemset[key]

	threeitemcf = {}
	for item in threeitemset:
			items = item.split(",")
			# calculate confidence of itemsets of size three
			threeitemcf[items[0] + ", " + items[1] + " --> " + items[2]] = threeitemset[item] / float(twoitemset[items[0] + "," + items[1]])
			threeitemcf[items[0] + ", " + items[2] + " --> " + items[1]] = threeitemset[item] / float(twoitemset[items[0] + "," + items[2]])
			threeitemcf[items[1] + ", " + items[2] + " --> " + items[0]] = threeitemset[item] / float(twoitemset[items[1] + "," + items[2]])

	# sort itemsets of size two based on helper function		
	sorted_threeitemcf = sorted(threeitemcf.items(), cmp = sortedhelper)

	# print top 5 rules with corresponding confidence scores in decreasing order of confidence score for itemsets of size three
	for i in range(1, 6):
		print sorted_threeitemcf[-i]

if __name__ == "__main__":
	oneitemset = oneitemset('browsing.txt')
	twoitemset = twoitemset(oneitemset, 'browsing.txt')
	threeitemset(twoitemset, 'browsing.txt')