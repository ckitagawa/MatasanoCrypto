import bitarray
import binascii
import base64
import string
import re
import numpy as np
from collections import Counter

str1 = "this is a test"
str2 = "wokka wokka!!!"

KEYSIZE = range(2, 42)

with open("file.txt", "r") as myfile:
	teststr = myfile.readlines()

a = str.join("", teststr)

def hamming(str1, str2):
	bits1 = bitarray.bitarray()
	bits1.fromstring(str1)
	bits2 = bitarray.bitarray()
	bits2.fromstring(str2)
	main = []
	for a, b in zip(bits1, bits2):
		if a == b:
			main.append(0)
		else:
			main.append(1)
	return sum(main)

def score(decstr):
  freq = {'E':12.02,'T':9.1,'A':8.12,'O':7.68,'I':7.31,'N':6.95,'S':6.28,'R':6.02,'H':5.92,'D':4.32,'L':3.98,'U':2.88,'C':2.71,'M':2.61,'F':2.3,'Y':2.11,'W':2.09,'G':2.03,'P':1.82,'P':1.82,'B':1.49,'V':1.11,'K':0.69,'X':0.17,'Q':0.11,'J':0.1,'Z':0.07}
  regex = re.compile('[^a-zA-Z]')
  no = len(decstr)
  decstr = regex.sub('', decstr)
  cnt = Counter(decstr.upper())
  variance = []
  n = len(decstr)
  penalty = (no - n) * 4
  if n != 0:
    for letter in string.ascii_uppercase:
      try:
        variance.append(abs(freq[letter] - cnt[letter] * 100 / n))
      except KeyError:
        variance.append(freq[letter])
  else:
    variance = [100 * 26]
  variance = (sum(variance) + penalty)/ 26 
  return variance

def decipher(instr):
  #bytes1 = bytearray(instr.encode("utf8"))
  bytes1 = instr
  minvar = 100
  strout = []
  for one in "0123456789abcdef":
    for two in "0123456789abcdef":
      char = str.join("", [one, two])
      bytes2 = bytes(binascii.unhexlify(char.encode("utf8") * (len(instr))))
      main = []
      for a, b in zip(bytes1, bytes2):
        main.append(a ^ b)
      obytes = bytearray(main)
      ostr = obytes.decode("utf8")
      scr = score(ostr)
      if scr <= minvar:
        minvar = scr 
        outputstr = ostr
        outputkey = binascii.unhexlify(char)
  return outputstr, outputkey

def XOR_Rep_Decrypt(instring, KEYSIZES):
  bytes1 = base64.urlsafe_b64decode(instring)
  mdist = 8 * max(KEYSIZES)
  for KEYSIZE in KEYSIZES:
    distances = 0
    for i in range(0, 50, 2):
      distances += hamming(bytes1[i*KEYSIZE:(i+1)*KEYSIZE].decode("utf8"), bytes1[(i+1)*KEYSIZE:(i+2)*KEYSIZE].decode("utf8"))/KEYSIZE
    distances = distances / (50 / 2)
    if distances < mdist:
      probable_size = KEYSIZE
      mdist = distances
  blocks = [bytes1[i:probable_size+i] for i in range(0, len(bytes1), probable_size)]
  blocks[-1] = blocks[-1] + binascii.unhexlify("00") * (probable_size - len(blocks[-1]))
  arr = []
  for block in blocks:
    arr.append([block[i:1+i] for i in range(0, len(block))])
  arr = np.array(arr)
  arr = np.transpose(arr)
  arr = arr.tolist()
  blocks = []
  for block in arr:
    tmp = bytes()
    for i in range(0, len(block)):
      tmp += block[i]
    blocks.append(tmp)
  full_key = bytearray()
  tmpstr = ""
  for block in blocks:
    tmpst, keyval = decipher(block)
    full_key += keyval
  okey = full_key.decode("utf8")
  return full_key.decode("utf8"), decrypt(bytes1.decode("utf8"), okey)

def decrypt(line1, key):
  bytes1 = bytearray(line1.encode("utf8"))
  bytes2 = bytearray(key.encode("utf8"))
  lngkey = (bytes2 * ((len(bytes1)//len(bytes2))+1))[:len(bytes1)]
  main = []
  for a, b in zip(bytes1, lngkey):
    main.append(a^b)
  obytes = bytearray(main)
  return obytes.decode("utf8")
  

print(XOR_Rep_Decrypt(a, KEYSIZE))
