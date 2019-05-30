print('Decorator')
def foo(f):
	def wrapped(numbers):
		print(numbers)
		return f(numbers)
	return wrapped
	
@foo
def summator(numbers):
	return(sum(numbers))
	
print(summator([1,2,3]))

print('\nList comprehensive')
i = [j ** i for i in range(10) for j in [2, 3] if i % 2 == 0]
print(sorted(i))


print('\nGenerator')
def odd_range(start, end):
	cur = start + 1 if start % 2 == 0 else start
	while cur < end:
		yield cur
		cur += 2

for number in odd_range(2, 10):
	print(number)
	
ranger = odd_range(2, 10)
print(ranger)
print(next(ranger))
print(next(ranger))


print('\nProperty')
class Robot:
	def __init__(self, power):
		self._power = power

	power = property()

	@power.setter
	def power(self, value):
		if value < 0:
			self._power = 0
		else:
			self._power = value

	@power.getter
	def power(self):
		return self._power

	@power.deleter
	def power(self):
		print('make robot useless')
		del self._power

	@property
	def c(self):
		return 6

walle = Robot(100)
print(walle.power)
walle.power = -20
print(walle.power)
del walle.power
print(walle.c)