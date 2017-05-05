"""
File: AStar.py

Description: A* Search Algorithm
	Keeps a map of the environment and uses it to perform the A* search algorithm

	The map is a grid, where each square records the number of times 
	an obstacle or line has been detected in that tile. A* can run on
	this map. If no path can be found, a threshold is increased so that
	tiles with only a few detections are assumed to be clear.
"""

import math
import heapq
import numpy as np
from functools import total_ordering

@total_ordering
class Cell(object):
	def __init__(self, x, y):
		# f is the heuristic cost
		self.points = 0
		self.x = x
		self.y = y
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0

	# toString method called by print()
	def __repr__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

	# Comparison methods
	def __eq(self, other):
		return (self.f == other.f)
	def __lt__(self, other):
		return (self.f < other.f)

class AStar(object):
	def __init__(self, map_width, map_height, vehicle_size):
		self.map_width = map_width
		self.map_height = map_height
		self.xscale = vehicle_size
		self.yscale = vehicle_size

		self.grid_width = int(self.map_width/self.xscale)
		self.grid_height = int(self.map_height/self.yscale)
		self.frontier = []		# open list
		heapq.heapify(self.frontier)
		self.explored = set()	# explored list
		self.grid = []
		self.threshold = 1

		self.last_data_set = []

		# initialize grid
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				self.grid.append(Cell(x, y))

	# Save points the sensors have seen
	def record_data(self, r, current_location, current_direction):
		positions = []
		for i in range(181):
			angle = (current_direction - 90 + i) % 360

			# Draw obstacle points seen
			x = current_location[0] + (r[i])*np.cos(angle*np.pi/180)
			y = current_location[1] - (r[i])*np.sin(angle*np.pi/180)
			positions.append((x, y))

			# Fix when cos and sin run past image limits
			if x < 0:
				x = 0
			if y < 0:
				y = 0
			if x > self.map_width:
				x = self.map_width-1
			if y > self.map_height:
				y = self.map_height-1

			# Increase likelihood that grid tile has an obstacle
			self.get_cell(math.floor(x/self.xscale), math.floor(y/self.yscale)).points += 1

		self.last_data_set = positions

	def set_start(self, start):
		self.start = self.get_cell(*start)

	def set_goal(self, goal):
		self.goal = self.get_cell(*goal)

	# Calculate heuristic value of cell (manhattan distance), slightly greedy
	def get_heuristic(self, cell):
		return 6*(abs(cell.x - self.goal.x) + abs(cell.y - self.goal.y))

	# Return a cell
	def get_cell(self, x, y):
		return self.grid[x * self.grid_height + y]

	# Get list of valid neightbors to a cell
	def get_adjacent_cells(self, cell):
		neighbors = []
		if cell.x < self.grid_width - 1:
			if cell.y < self.grid_height - 1:
				neighbors.append(self.get_cell(cell.x + 1, cell.y + 1)) # down right
			neighbors.append(self.get_cell(cell.x + 1, cell.y))	# right
			if cell.y > 0:
				neighbors.append(self.get_cell(cell.x + 1, cell.y - 1)) # up right

		if cell.y > 0:
			neighbors.append(self.get_cell(cell.x, cell.y - 1)) # up

		if cell.x > 0:
			if cell.y > 0:
				neighbors.append(self.get_cell(cell.x - 1, cell.y - 1)) # up left
			neighbors.append(self.get_cell(cell.x - 1, cell.y)) # left
			if cell.y < self.grid_height - 1:
				neighbors.append(self.get_cell(cell.x - 1, cell.y + 1)) # down left

		if cell.y < self.grid_height - 1:
			neighbors.append(self.get_cell(cell.x, cell.y + 1)) # down

		return neighbors

	# Trace parents back to start and then reverse the path
	def get_path(self):
		cell = self.goal
		path = [(cell.x, cell.y)]
		while cell.parent is not self.start:
			cell = cell.parent
			path.append((cell.x, cell.y))

		path.append((self.start.x, self.start.y))
		path.reverse()
		return path

	# Calculate data for cell
	def update_cell(self, adj, cell):
		adj.g = cell.g + 5
		adj.h = self.get_heuristic(adj)
		adj.parent = cell
		adj.f = adj.h + adj.g

	# Find a path through a grid
	def solve(self):
		# Add starting cell to open heap queue
		heapq.heappush(self.frontier, (self.start.f, self.start))

		while len(self.frontier):
			# Pop cell from heap queue
			f, cell = heapq.heappop(self.frontier)
			# Add cell to explored list so we don't process it twice
			self.explored.add(cell)

			# If ending cell, return found path
			if cell is self.goal:
				return self.get_path()

			# Get adjacent cells for cell
			adj_cells = self.get_adjacent_cells(cell)
			for adj_cell in adj_cells:
				if adj_cell.points < self.threshold and adj_cell not in self.explored:
					if (adj_cell.f, adj_cell) in self.frontier:
						# If adj cell in open list, check if current path is better than the one previously found for this adj cell
						if adj_cell.g > cell.g + 5:
							self.update_cell(adj_cell, cell)
					else:
						self.update_cell(adj_cell, cell)
						# add adj cell to open list
						heapq.heappush(self.frontier, (adj_cell.f, adj_cell))

		if self.threshold < 50:
			self.threshold += 5
			return self.solve()

# Test run
if __name__ == "__main__":
	a = AStar(3048, 6096, 89)
	a.set_start((1, 1))
	a.set_goal((10, 10))

	# Trap robot with walls
	a.get_cell(1, 2).points += 5
	a.get_cell(2, 1).points += 5
	a.get_cell(2, 2).points += 5
	a.get_cell(2, 0).points += 5
	a.get_cell(0, 2).points += 5

	path = a.solve()	# Find a path
	print(path)
	print(a.threshold)
