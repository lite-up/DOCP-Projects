import itertools

def imright(h1, h2):
    # House h1 is immediately right of h2 if h1-h2 == 1."
    return h1-h2 == 1

def nextto(h1, h2):
    # Two houses are next to each other if they differ by 1."
    return abs(h1-h2) == 1

def zebra_puzzle_fast():
	# Return a tuple (WATER, ZEBRA) indicating their house numbers
	houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
	orderings = list(itertools.permutations(houses))	#1
	return next((WATER, ZRBRA)
		for (red, green, ivory, yellow, blue) in orderings
		if imright(green, ivory)		#6
		for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in orderings
		if Englishman == red			#2
		if Norwegian == first			#10
		if nextto(Norwegian, blue)		#15
		for (coffee, tea, milk, oj, WATER) in orderings
		if coffee == green				#4
		if Ukranian == tea				#5
		if milk == middle				#9
		for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in orderings
		if Kools == yellow				#8
		if LuckyStrike == oj			#13
		if Japanese == Parliaments		#14
		for (dog, snails, fox, horse, ZEBRA) in orderings
		if Spaniard == dog				#3
		if OldGold == snails			#7
		if nextto(Chesterfields, fox)	#11
		if nextto(Kools, horse)			#12
		)
		
def timedcall(fn, *args):
	# Call function with args; return the time in seconds and result
	t0 = time.clock()
	result = fn(*args)
	t1 = time.clock()
	return t1-t0, result
	
def timedcalls_backup(n, fn, *args):
	# Call function n times with args; return the min, avg, and max time
	times = [timedcall(fn, *args)[0] for _ in range(n)]
	return min(times), average(times), max(times)
	
def timedcalls(n, fn, *args):
	# Call fn(*args) repeatedly: n times if n is an int, or up to
	# n seconds if n is a float; return the min, avg, and max time
	if isinstance(n, int):
		times = [timedcall(fn, *args)[0] for _ in range(n)]
	else:
		times = []
		while sum(times) < 10.0:
			times.append([timedcall(fn, *args)[0]])
	return min(times), average(times), max(times)
			
def average(numbers):
	# Retuen the average (arithmetic mean) of a sequence of numbers
	return sum(numbers) / float(len(numbers))
	
def instrument_fn(fn, *args):
	c.starts, c.items = 0, 0
	result = fn(*args)
	print "%s got %s with %5d iters over %7d items" % (
		fn.__name__, result, c.starts, c.items)