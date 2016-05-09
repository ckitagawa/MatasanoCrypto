import binascii
import struct
import math

key = "YELLOW SUBMARINE"

def PCKS7(keystr, length): 
	diff = length - len(key)
	if diff < 0:
		return 0
	padding = bytes([diff]) * diff
	pkey = key.encode("utf8")  + padding
	return pkey

def keylength(key, file):
	f = len(file.encode("utf8"))
	k = len(key.encode("utf8"))
	k1 = k + 256
	k2 = k
	if f > k:
		while f / 2 >= k and k < k1:	
			if f % k == 0:
				return k
			k += 1
		if (f/2 < k and (f - k2) < 256):
			return f
		else: 
			return 0
	else:
		return 0
	
a = "a" * 271
b = keylength(key, a)

print(b)
print(PCKS7(key, b))