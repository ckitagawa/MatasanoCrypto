import base64
import binascii

base16str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
base64str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

def hexto64(hexStr):
  bytes = binascii.a2b_hex(hexStr)
  return base64.b64encode(bytes)

result = hexto64(base16str)
print(result.decode("utf-8"))
if (result.decode("utf-8") == base64str):
  print("Success")