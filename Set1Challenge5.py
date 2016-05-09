import binascii

check1 = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

line1 = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"

def encrypt(line, key):
	bytes1 = bytearray(line1.encode("utf8"))
	bytes2 = bytearray(key.encode("utf8"))
	lngkey = (bytes2 * ((len(bytes1)//len(bytes2))+1))[:len(bytes1)]
	main = []
	for a, b in zip(bytes1, lngkey):
		main.append(a^b)
	bytes = bytearray(main)
	return binascii.hexlify(bytes)
	
a = encrypt(line1, key)
print(a.decode("utf8"))
if (check1 == a.decode("utf8")):
	print("Success")
