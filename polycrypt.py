from polynomial import Polynomial
from Crypto.Util import number
import os

class PolyArgument(Polynomial):
	def __init__(self, coefs, refresh_key, o):
		super().__init__(coefs)
		self.refresh = refresh_key
		self.o = o

	def __and__(self, other):
		assert(isinstance(other, PolyArgument))

		out = self.tmul(other)
		out.refresh = self.refresh
		out.o = self.o

		return out % self.refresh

	def __xor__(self, other):
		assert(isinstance(other, PolyArgument))

		out = self + other
		out.refresh = self.refresh
		out.o = self.o

		return out % self.refresh

	def __invert__(self):
		out = self + self.o
		out.refresh = self.refresh
		out.o = self.o

		return out % self.refresh

class Polycrypt:
	def __init__(self, security=128, key=None):
		self.security = security

		if key:
			self.key = key
		else:
			self._gen_key()

		self._gen_refresh()

	def _rand(self):
		return int.from_bytes(os.urandom(self.security // 8), byteorder='big')

	def _gen_key(self):
		self.key = number.getPrime(self.security, os.urandom)

	def _gen_refresh(self):
		self.refresh = self.key * (self._rand() & ~1)

	def _encrypt(self, message):
		m = Polynomial.from_number(message)
		n = len(m)
		
		y = Polynomial(list(map(lambda x: (x + self.key * self._rand()), m.raw_coefs)))
		
		assert(y % self.key == m)

		d = Polynomial(list(map(lambda x: self._rand(), range(n))))

		return (y + d * self.key).raw_coefs

	def encrypt(self, message):
		# Generate correct bitlength of 1s
		count = len(bin(message)) - 2
		one = int('1' * count, 2)

		# Encrypt the ones and message
		_enc = self._encrypt(message)
		_one = self._encrypt(one)

		# Make a self refrential one polyarg
		one = PolyArgument(_one, self.refresh, None)
		one.o = one

		# Make the enc polyarg with the one
		return PolyArgument(_enc, self.refresh, one)

	def decrypt(self, poly):
		poly = (poly % self.key) % 2
		return int(''.join(map(str, poly.raw_coefs))[::-1], 2)

if __name__ == "__main__":
	x = 0xDEADBEEF
	y = 4

	poly = Polycrypt()
	o = poly.encrypt(0xFF)
	a = poly.encrypt(x)
	b = poly.encrypt(y)

	print(bin(x))
	print(bin(poly.decrypt(~a)))
	# print((~x & ~y))