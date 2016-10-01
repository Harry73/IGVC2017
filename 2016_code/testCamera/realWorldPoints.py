output = "realWorldPoints = array("
z = 2

for y in range(2,7):
	for x in range(-1, z):
		output = output + "[" + str(x*2*12) + "," + str((y*2 + 1)*12) + ",0],"
		
output = output[:-1]
output = output + ")"
print(output)
