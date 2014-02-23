#!/usr/bin/python3.3
"""Module for managing a graph representing a ski resort"""

class Point(object):
	"""This class provides an object representing a point in the ski resort"""
	def __init__(self, number, name, altitude):
		"""
			Initialize a Point object with a number, a name and an altitude
			:param number: The number of the Point
			:type number: string
			:param name: The name of the Point
			:type name: string
			:param altitude: The altitude of the Point
			:type altitude: string
		"""
		self.number = int(number)
		self.name = name
		self.altitude = int(altitude)
		
	def __str__(self):
		"""
			Returns a printable version of the object
		
			:return: "n:[self.number] name:[self.name] alt:self.altitude"
			:rtype: string
		"""
		return "n:{} name:{} alt:{}".format(self.number, self.name, self.altitude)

class Route(object):
	"""This class provides an object representing a route (ropeway, bus, slope, ...) from a point to an other in the ski resort """
	def __init__(self, number, name, _type, start, end):
		"""
			Initialize the Route object
		
			:param number: the number of the Route
			:type number: string
			:param name: the name of the Route
			:type name: string
			:param _type: the type of the Route (ropeway, bus, slope, ...)
			:type _type: string
			:param start: the Point from where the Route starts
			:type start: Point
			:param end: the Point to where the Route ends
			:type end: Point
		"""
		self.number = int(number)
		self.name = name
		self._type = _type
		self.start = start
		self.end = end
		'''Defining duration of the route in seconds thanks to its type, its starting and ending points'''
		if _type=="BUS":
			if (start.name=="arc1600" and end.name=="arc1800") or (end.name=="arc1600" and start.name=="arc1800"):
				self.time = 30.0;
			else:
				self.time = 40.0;
		elif _type == "V" or _type == "B" or _type == "R" or _type == "N" or _type == "KL" or _type == "SURF" :
			if _type == "V":
				coeff = 5.0
			elif _type == "B":
				coeff = 4.0
			elif _type == "R":
				coeff = 3.0
			elif _type == "N":
				coeff = 2.0
			elif _type == "KL":
				coeff = 1.0/6
			else:
				coeff = 10.0
			self.time = coeff*(start.altitude-end.altitude)/100.0
		else:
			if _type == "TPH":
				coeff = 2.0
				add = 4.0
			elif _type == "TC":
				coeff = 3.0
				add = 2.0
			elif _type == "TSD":
				coeff = 3.0
				add = 1.0
			else:
				coeff = 4.0
				add = 1.0
			self.time = coeff*(end.altitude-start.altitude)/100.0 + add
	def __str__(self):
		"""
			Return a printable version of the object
		
			:return: "[self._type] "[self.name]"(n°[self.number]) from:"[self.start.name]"(n°[self.start.number]) to "[self.end.name]"(n°[self.end.number]) during [self.time]min[self.time]sec"
			:rtype: string
		"""
		return "{} \"{}\"(n°{}) from:\"{}\"(n°{}) to \"{}\"(n°{}) during {}min{}sec".format(self._type, self.name, self.number, self.start.name, self.start.number, self.end.name, self.end.number, int(self.time),int(self.time%1*60))

class Graph(object):
	"""This class provides an object representing the whole set of routes and points in the ski resort"""
	def __init__(self, points, routes):
		"""
			Initialize the Graph object
		
			:param points: the whole set of points in the ski resort
			:type points: list of Point
			:param routes: the whole set of routes in the ski resort
			:type routes: list of Route
		"""
		self.points = points
		self.routes = routes
				
	def applyFloydWarshallAlgorithm(self):
		"""
			Apply the Floyd-Warshall algorithm on the graph and store the result in two matrices: one with the duration between two points and one with the intermediate between two points
		"""
		size = len(self.points)
		self.floydWarshall = [[0] * size for _ in range(size)]
		self.next = [[-1] * size for _ in range(size)]
		for route in self.routes:
			if self.floydWarshall[route.start.number-1][route.end.number-1] == 0 or self.floydWarshall[route.start.number-1][route.end.number-1]>route.time:
				self.floydWarshall[route.start.number-1][route.end.number-1] = route.time
				self.next[route.start.number-1][route.end.number-1]=route.end.number-1

		for k in range(size):
			for i in range(size):
				for j in range(size):
					if self.floydWarshall[i][j] > self.floydWarshall[i][k] + self.floydWarshall[k][j] and self.floydWarshall[i][k]!=0 and self.floydWarshall[k][j]!=0 or (self.floydWarshall[i][j]==0 and i!=j and self.floydWarshall[i][k]!=0 and self.floydWarshall[k][j]!=0):
						self.floydWarshall[i][j] = self.floydWarshall[i][k] + self.floydWarshall[k][j]
						self.next[i][j] = k
					
	def getShortestPathWithFloydWarshall(self, start, end):
		"""Retrieve the shortest path thanks to the matrix of intermediates between two points
		
			This function will retrieve the shortest path (if it exists) between two points of the ski resort thanks to the matrix of intermediates
			:param start: The number of the starting point of the trip
			:type start: int
			:param end: The number of the ending point of the trip
			:type end: int
			:return: The shortest path between two points of the ski resort thanks to the Floyd-Warshall algorithm
			:rtype: string			
		"""
		global shortestRoute
		shortestRoute=""
		if self.next[start][end]==-1:
			return "No existing path between {} and {}".format(start, end)
		'''Check whether the path is direct or not'''
		if self.next[start][end]==end:
			'''Find the shortest route between these two points'''
			for route in self.routes:
				if route.start.number-1==start and route.end.number-1==end:
					shortestRoute = route
					break
			for route in self.routes:
				if route.start.number-1==start and route.end.number-1==end:
					if shortestRoute.time > route.time:
						shortestRoute = route
			return str(shortestRoute)
		'''There is no direct path between these two points but there exists a path thanks to one or more intermediate'''
		return "{}\nTake {}".format(self.getShortestPathWithFloydWarshall(start, self.next[start][end]), self.getShortestPathWithFloydWarshall(self.next[start][end], end))	
	def DFS(self,point):
		"""Apply the DFS algorithm on the graph to find all reachable points from the point and store them in an attribute
			:param point: The Point from which we are looking for reachable points
			:type point: Point
		"""
		self.reachable_points.append(point)
		for route in self.routes:
			if route.start.number == point and route.end.number not in self.reachable_points:
				self.DFS(route.end.number)
				
	def getReachableDestination(self, start):
		"""Initialize the DFS attribute of the graph and launch the DFS on it
			:param start: The Point from which we are looking for reachable points
			:type start: Point
		"""
		self.reachable_points = list()		
		self.DFS(start)		
		return self.reachable_points
		
points_list = list()
routes_list = list()
source=open("dataski.txt", "r")
"""Parse the input formatted map"""
_size = int(source.readline())
for i in range(_size):
	line = source.readline().split("\t")
	del line[3:len(line)]
	points_list.append(Point(*line))

_size = int(source.readline())
for i in range(_size):
	line = source.readline().replace("\n","")
	line = line.split("\t")
	line[3]=points_list[int(line[3])-1]
	line[4]=points_list[int(line[4])-1]
	routes_list.append(Route(*line))
source.close()
"""Create the associated graph"""
g = Graph(points_list, routes_list)
"""Create the Floyd-Warshall matrices"""
g.applyFloydWarshallAlgorithm()
"""Ask for a trip and give the shortest path (if it exists)"""
while True:
	start = int(input("Please enter the point where you will start:"))
	end = int(input("Please enter the point where you will end:"))
	if not (start<=0 or end<=0 or start>len(points_list) or end>len(points_list)):
		break
print("\nEstimated time from {} to {}: {}min{}sec\nTake {}\n\n\n\n".format(points_list[start-1].name, points_list[end-1].name,int(g.floydWarshall[start-1][end-1]),int(g.floydWarshall[start-1][end-1]%1*60),g.getShortestPathWithFloydWarshall(start-1,end-1)))

"""Delete routes which doesn't correspond to the user's level"""
skier_type = input("Are you a snowboarder or a skier? (SURF/SKI)").upper()
while skier_type!="SURF" and skier_type!="SKI":
	skier_type = input("Are you a snowboarder or a skier? (SURF/SKI)").upper()
if skier_type=="SKI":
	not_allowed="SURF"
	while True:
		level = input("Please enter your skiing skills: (V/B/R/N/KL) and we will only give you routes that match your skiing level!").upper()
		if (level in "VBRN" and len(level)==1) or level=="KL":
			print("You chose {}".format(level))
			break
else:
	not_allowed="KL"
	while True:
		level = input("Please enter your skiing skills: (V/B/R/N) and we will only give you routes that match your skiing level!").upper()
		if level in "VBRN" and len(level)==1:
			print("You chose {}".format(level))
			break
"""Delete routes which doesn't correspond to the user's choices"""
exception_list =  input("Please enter name of each route you don't want to take separated with a space or leave blank if you don't care about taken routes:").split()
skills_routes = list()
skills_routes.extend(routes_list)
for route in routes_list:
	if route._type==not_allowed:
		skills_routes.remove(route)
	elif route._type=="KL" and level!="KL":
		skills_routes.remove(route)	
	elif route._type=="N" and level!="N" and level!="KL":
		skills_routes.remove(route)
	elif route._type=="R" and (level=="V" or level=="B"):
		skills_routes.remove(route)
	elif route._type=="B" and level=="V":
		skills_routes.remove(route)
	elif route.name in exception_list:
		skills_routes.remove(route)
while True:
	start = int(input("Please enter the point where you will start:"))
	if not(start<=0 or start>len(points_list)):
		break
g.routes = skills_routes
"""Give all reachable points matching the user's level or choices from the given starting point"""
print("Reachable destinations from {}:".format(start))
print(g.getReachableDestination(start))
