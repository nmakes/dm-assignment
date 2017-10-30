#DBScan
#Written By Naveen Venkat

import math

class point:
	
	'''
		Definitions:

		Compatible points - two points with the same number and type of attributes
	'''

	oneHotDistance = 1
	epsRadius = 
	def __init__(self, ATTR= None, TYPE = None):
		'''
			Sample ATTR :-
			ATTR = { 'height':['cont', 168], 'name':['nom', 'naveen'], 'rank':['ord', 12]}
		'''
		self.ATTR = ATTR
		self.TYPE = TYPE	# core, boundary or noise

	def __repr__(self):
		return self.TYPE, " : ", self.ATTR

def distance(point1, point2, opt='euclidean'):	# assume compatible points
	
	dist = None

	if opt=='euclidean':
		
		distSquare = 0
		oneHotDist = 0

		for attr in point1.ATTR:
			if attr not in point2.ATTR.keys():
				print "ERROR: Incompatible Points"
				return None
			elif point1.ATTR[attr][0] != point2.ATTR[attr][0]:
				print "ERROR: Incompatible Points"
				return None
			else:
				if ( (point1.ATTR[attr][0]=='cont') | (point1.ATTR[attr][0]=='ord')):
					distSquare += (point1.ATTR[attr][1] - point2.ATTR[attr][1]) ** 2
				elif (point1.ATTR[attr][0]=='nom'):
					oneHotDist += point.oneHotDistance
		dist = math.sqrt(distSquare)
		dist += oneHotDist
		return dist

point1 = point({
					'height':['cont', 168],
					'weight':['cont', 70],
					'name':['nom','nav']
				})
point2 = point({
					'height':['cont', 165],
					'weight':['cont', 74],
					'name':['nom','van']
				})

print distance(point1, point2)

def dbsScan(pointList):
	
	for point in pointList:
