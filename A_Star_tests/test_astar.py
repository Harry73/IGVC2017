from AStar import AStar

map = 3

def main():
	a = AStar()
	i = 0
	walls = []
	with open("Maps/map" + str(map) + ".txt", "r") as f:
		size = f.readline()
		for line in f:
			j = 0
			for char in line:
				if char == '#':
					walls.append((j, i))
				elif char == 's':
					start = (j, i)
				elif char == 'g':
					goal = (j, i)
				j += 1
			i += 1

	size = size.split()
	a.init_grid(int(size[0]), int(size[1]), walls, start, goal)
	#a.set_cell(5, 8, False)
	path = a.solve()
	print(path)
	
if __name__ == "__main__":
	main()