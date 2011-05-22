# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import hashlib
import base64
import os


# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = chr(0)

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

secret = 'koRie$r9k%ohmu&Ayouk)9Q"uoo§souifo4*aex4u#Basheek*a9jooHuoG/heiqua7oPh'
key = hashlib.sha256(secret).digest()

def encodeAES(msg):
	cipher = AES.new(key)
	return base64.b64encode(cipher.encrypt(pad(msg)))

def decodeAES(cmsg):
	cipher = AES.new(key)
	return cipher.decrypt(base64.b64decode(cmsg)).rstrip(PADDING)


# encode a string
#encoded = encodeAES('password{asfasönfnlanfas"$°"$"%&/(%)/(%$"§!ÄÖÄ*$!$!')
#print 'Encrypted string:', encoded

# decode the encoded string
#decoded = decodeAES(encoded)
#print 'Decrypted string:', decoded
