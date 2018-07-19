class Polynomial:
	def __init__(self, coefs):
		assert(isinstance(coefs, list))

		self.raw_coefs = coefs
		self.coefs = zip(coefs, range(len(coefs)))
		self.red_coefs = list(filter(lambda tpl: tpl[0] != 0, self.coefs))

	@staticmethod
	def from_number(number):
		return Polynomial(list(map(int, bin(number)[2:]))[::-1])

	def __call__(self, x):
		assert(type(x) == int)
		return sum(map(lambda tpl: tpl[0] * (x ** tpl[1]), self.red_coefs))

	def __repr__(self):
		return 'Polynomial([' + ', '.join(self.coefs) + '])'

	def __str__(self):
		return ' + '.join(map(lambda tpl: str(tpl[0]) + 'x^' + str(tpl[1]), list(self.red_coefs)[::-1]))

	def __add__(self, other):
		assert(isinstance(other, Polynomial))

		a = self.raw_coefs
		b = other.raw_coefs

		if len(a) < len(b):
			a = a + [0] * (len(b) - len(a))
		elif len(b) < len(a):
			b = b + [0] * (len(a) - len(b))

		return Polynomial(list(map(lambda x: sum(x), zip(a, b))))

	def __mul__(self, other):
		assert(isinstance(other, Polynomial) or isinstance(other, int))

		if isinstance(other, Polynomial):
			a = self.raw_coefs
			b = other.raw_coefs

			output = [0] * (len(a) + len(b) - 1)

			for i in range(len(a)):
				for j in range(len(b)):
					output[i + j] += a[i] * b[j]

			return Polynomial(output)
		elif isinstance(other, int):
			return Polynomial(list(map(lambda x: x * other, self.raw_coefs)))

	def __mod__(self, other):
		assert(isinstance(other, int))
		return Polynomial(list(map(lambda x: x % other, self.raw_coefs)))

	def __len__(self):
		return len(self.raw_coefs)

	def __eq__(self, other):
		return self.red_coefs == other.red_coefs