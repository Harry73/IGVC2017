import math
import heapq
from functools import total_ordering

@total_ordering
class Cell(object):
	def __init__(self, x, y):
		# f is the heuristic cost
		self.reachable = True
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
	def __init__(self):
		self.frontier = []		# open list
		heapq.heapify(self.frontier)
		self.explored = set()	# explored list
		self.grid = []
		self.grid_height = None
		self.grid_width = None

	# Set up a new grid
	def init_grid(self, width, height, obstacles, start, goal):
		self.grid_height = height
		self.grid_width = width

		# initialize grid
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				self.grid.append(Cell(x, y))

		# Set up any obstacles
		for obstacle in obstacles:
			self.get_cell(obstacle[0], obstacle[1]).reachable = False

		self.start = self.get_cell(*start)
		self.goal = self.get_cell(*goal)

	# Calculate heuristic value of cell (manhattan distance)
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
			print(cell)
			# Add cell to explored list so we don't process it twice
			self.explored.add(cell)

			# If ending cell, return found path
			if cell is self.goal:
				return self.get_path()

			# Get adjacent cells for cell
			adj_cells = self.get_adjacent_cells(cell)
			for adj_cell in adj_cells:
				if adj_cell.reachable and adj_cell not in self.explored:
					if (adj_cell.f, adj_cell) in self.frontier:
						# If adj cell in open list, check if current path is better than the one previously found for this adj cell
						if adj_cell.g > cell.g + 5:
							self.update_cell(adj_cell, cell)
					else:
						self.update_cell(adj_cell, cell)
						# add adj cell to open list
						heapq.heappush(self.frontier, (adj_cell.f, adj_cell))
