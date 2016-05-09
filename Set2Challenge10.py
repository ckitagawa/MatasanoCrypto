import binascii
import string
import random
import base64
from Crypto.Cipher import AES 

key = "YELLOW SUBMARINE"

with open("10.txt", "r") as myfile:
	text = myfile.readlines()
mtext = ""
for line in text:
	mtext += line.rstrip()

def PCKS7(key, length): 
	diff = length - len(key)
	if diff < 0:
		return 0
	padding = bytes([diff]) * diff
	pkey = key.encode("utf8")  + padding
	return pkey

def keylength(text, key):
	f = len(text)
	k = len(key)
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

def check(text, key):
	mod = len(text) % len(key) 
	if mod == 0:
		return key
	else:
		return PCKS7(key, keylength(text, key))

def IV(length, mode):
	if mode == 0:
		return bytearray("0".encode("utf8")) * length
	else:
		chars = string.printable
		charcount = len(chars)
		nums = range(0, charcount)
		chardict = dict(zip(nums, chars))
		out = bytearray()
		for i in range(0, length):
			ch = chardict[random.randint(0, charcount - 1)]
			out += bytes([ch])
		return out

def XOR(text, key):
	out = bytearray()
	for a, b in zip(text, key):
		out += bytes([a ^ b])
	return out

def aesECBencrypt(text, key):
	cipher = AES.new(bytes(key), AES.MODE_ECB)
	msg = cipher.encrypt(bytes(text))
	return msg

def CBC_Decrypt(text, key, mode):
	#textbytes = bytearray(text.encode("utf8"))
	textbytes = base64.b64decode(text)
	keybytes = bytearray(key.encode("utf8"))
	keybytes = check(textbytes, keybytes)
	lenkey = len(keybytes)
	repeats = len(textbytes) // lenkey
	ivbytes = IV(len(keybytes), mode)
	maincipher = bytearray()
	chiphertext = XOR(ivbytes, keybytes)
	for i in range(0, repeats):
		chiphertext = aesECBencrypt(XOR(textbytes[i * lenkey:(i + 1) * lenkey], chiphertext), keybytes)
		maincipher += chiphertext
	return maincipher.decode("latin-1")

print(CBC_Decrypt(mtext, key, 0))