def all_ints():
	# Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ....
	i = 0
	cnt = 1
	while True:
		yield i
		if cnt % 2 == 0:
			i -= cnt
		else:
			i += cnt
		cnt += 1
		
def ints(start, end=None):
	i = start
	while i <= end or end == None:
		yield i
		i += 1
		
def all_ints_teach_2():
	yield 0
	for i in ints(1):
		yield +i
		yield -i
			
def all_ints_teach():
	yield 0
	i = 1
	while True:
		yield +i
		yield -i
		i += 1