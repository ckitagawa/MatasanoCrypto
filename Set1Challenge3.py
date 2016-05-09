import binascii
import string

encryption = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def scorev1(stringin):
  stringin = stringin.lower()
  freq = {i:stringin.count(i) for i in stringin}
  score = 0
  for i in "e":
    try:
      score += freq[i] * 3
    except KeyError:
      score += 0
  for i in "taoinshr":
    try:
      score += freq[i] * 2
    except KeyError:
      score += 0
  for i in "dl":
    try:
      score += freq[i]
    except KeyError:
      score += 0
  return score

def score(stringin, wlist):
  for k in wlist:
    if len(k.rstrip()) >= 4:
      if (k.lower().rstrip() in stringin.lower()):
        return 1
  return 0

def decipher1(stringin, wlist):
  bytes1 = binascii.a2b_hex(stringin)
  strout = []
  for i in "0123456789abcdef":
    for j in "0123456789abcdef":
      main = []
      bytes2 = binascii.a2b_hex(str.join('',[i,j]) * int(len(stringin)/2))
      for a, b in zip(bytes1, bytes2):
        main.append(a ^ b)
      bytes = bytearray(main)
      try:
        out = bytes.decode("latin-1")
      except UnicodeDecodeError:
        print('Error failed to decode: ', i, j)
      s = score(out, wlist)
      if s == 1:
        strout.append([out, i, j])
  return strout

def decipher(stringin, wlist):
  bytes1 = binascii.a2b_hex(stringin)
  top = 0
  strout = []
  for i in "0123456789abcdef":
    for j in "0123456789abcdef":
      main = []
      bytes2 = binascii.a2b_hex(str.join('',[i,j]) * int(len(stringin)/2))
      for a, b in zip(bytes1, bytes2):
        main.append(a ^ b)
      bytes = bytearray(main)
      out = bytes.decode("latin-1")
      s = score(out, wlist)
      if s > top:
        strout = out
        top = s
  return strout, top

wlist = list(open("words.txt", 'r'))
possibles, scr = decipher(encryption, wlist)
print(possibles)
