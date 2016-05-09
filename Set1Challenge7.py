import base64
from Crypto.Cipher import AES 

key = "YELLOW SUBMARINE"

with open("7.txt", "r") as myfile:
	teststr = myfile.readlines()

a = str.join("", teststr)	

def aesECBdecode(str, key):
	bytes1 = base64.b64decode(str)
	bytekey = bytes(key.encode("utf8"))
	cipher = AES.new(bytekey, AES.MODE_ECB)
	msg = cipher.decrypt(bytes1)
	return msg
	
b = aesECBdecode(a, key)
print(b.decode("utf8"))