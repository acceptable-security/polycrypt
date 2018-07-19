from polynomial import Polynomial
from Crypto.Util import number
import os

class PolyArgument(Polynomial):
	def __init__(self, coefs, refresh_key):
		super().__init__(coefs)
		self.refresh = refresh_key

	def __and__(self, other):
		assert(isinstance(other, PolyArgument))
		return (self.tmul(other)) % self.refresh

	def __xor__(self, other):
		assert(isinstance(other, PolyArgument))
		return (self + other) % self.refresh

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

	def encrypt(self, message):
		m = Polynomial.from_number(message)
		n = len(m)
		
		y = Polynomial(list(map(lambda x: (x + self.key * self._rand()), m.raw_coefs)))
		
		assert(y % self.key == m)

		d = Polynomial(list(map(lambda x: self._rand(), range(n))))

		return PolyArgument((y + d * self.key).raw_coefs, self.refresh)

	def decrypt(self, poly):
		poly = (poly % self.key) % 2
		d = poly.raw_coefs
		return int(''.join(map(str, d))[::-1], 2)

if __name__ == "__main__":
	x = 0xFF
	y = 0x21

	poly = Polycrypt()
	c1 = poly.encrypt(x)
	c2 = poly.encrypt(y)

	c3 = c1 ^ c2

	print(str(x) + ':\t' + bin(x)[2:])
	print(str(y) + ':\t' + bin(y)[2:])
	print('or:\t' + bin(x & y)[2:])
	print('us:\t' + bin(poly.decrypt(c3))[2:])

	# assert(bin(x ^ y)[2:] == bin(poly.decrypt(c3))[2:])