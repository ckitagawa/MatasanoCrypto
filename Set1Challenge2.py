import binascii

in1 = "1c0111001f010100061a024b53535009181c"
in2 = "686974207468652062756c6c277320657965"
test = "746865206b696420646f6e277420706c6179"

def fixedXOR(str1, str2):
  bytes1 = binascii.a2b_hex(str1)
  bytes2 = binascii.a2b_hex(str2)
  main = []
  for a, b in zip(bytes1, bytes2):
    main.append(a ^ b)
  bytes = bytearray(main)
  return binascii.hexlify(bytes)

result = fixedXOR(in1, in2)
print(result.decode("utf8"))
if (result.decode("utf-8") == test):
  print("Success")