import binascii
import string

def score(stringin, wlist):
  s = 0
  for k in wlist:
    if not "\\x" in stringin:
      if len(k.rstrip()) >= 3:
        if (k.lower().rstrip() in stringin.lower()):
          s += 1
  return s

def decipher(stringin, wlist, cnt):
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
  return strout, top, cnt

wlist = list(open("words.txt", 'r'))
encryptstrs = list(open("encrypt.txt", 'r'))
cnt = 1
s = 0
for n in encryptstrs:
  if len(n.rstrip()) % 2 == 0:
    res, scr, wh = decipher(n.rstrip(), wlist, cnt)
    if not res:
      cnt += 1
    else:
      if scr > s:
        possible = res
        s = scr
        num = wh
      cnt += 1
  else:
    print("Skipped: ", n)

print(possible, wh)
