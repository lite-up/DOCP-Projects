def zebra_puzzle_slow_solution():
	# Return a tuple (WATER, ZEBRA) indicating their house numbers
	houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
	orderings = list(itertools.permutations(houses))	#1
	return next((WATER, ZRBRA)
		for (red, green, ivory, yellow, blue) in orderings
		for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in orderings
		for (dog, snails, fox, horse, ZEBRA) in orderings
		for (coffee, tea, milk, oj, WATER) in orderings
		for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in orderings
		if Englishman == red			#2
		if Spaniard == dog				#3
		if coffee == green				#4
		if Ukranian == tea				#5
		if imright(green, ivory)		#6
		if OldGold == snails			#7
		if Kools == yellow				#8
		if milk == middle				#9
		if Norwegian == first			#10
		if nextto(Chesterfields, fox)	#11
		if nextto(Kools, horse)			#12
		if LuckyStrike == oj			#13
		if Japanese == Parliaments		#14
		if nextto(Norwegian, blue)		#15
		)
		