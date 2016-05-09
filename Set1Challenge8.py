import binascii

with open("8.txt", "r") as myfile:
	teststr = myfile.readlines()

def ECBdetect(line):
	BLOCKSIZE = 16
	bytes1 = binascii.unhexlify(line)
	splitbytes = [bytes1[i:i+BLOCKSIZE] for i in range(0, len(bytes1), BLOCKSIZE)]
	BLOCKS = len(splitbytes)
	likelihood = 0
	register = []
	for i in range(BLOCKS):
		a = splitbytes[i]
		if a not in register:
			for j in range(i + 1, BLOCKS):
				b = splitbytes[j]
				if a == b:
					likelihood += 1
					if a not in register:
						register.append(a)
	if register != []:
		for i in register:
			print(binascii.hexlify(i).decode("utf8"))
	return likelihood

cnt = 1	
top = 0
for line in teststr:
	line = line.rstrip()
	if len(line) % 2 != 0:
		print("Skipping odd line:", cnt)
	else:
		score = ECBdetect(line)
		if score != 0:
			print("Possible ECB line: ", cnt, " likelihood: ", score)
	cnt += 1	

