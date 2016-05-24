# zebra_puzzle的解决方法及引申

### A. 解题方法
今天用python来解决传说中的斑马难题

> 1. 英国人住在红色的房子里；
> 2. 西班牙人养了一条狗；
> 3. 日本人是一个油漆工；
> 4. 意大利人喜欢喝茶；
> 5. 挪威人住在左边的第一个房子里；
> 6. 绿房子在白房子的右边；
> 7. 摄影师养了一只蜗牛；
> 8. 外交官住在黄房子里；
> 9. 中间房子里的那个人喜欢喝牛奶；
> 10. 喜欢喝咖啡的人住在绿房子里；
> 11. 挪威人住在蓝色的房子旁边；
> 12. 小提琴家喜欢喝橘子汁；
> 13. 养狐狸的人所住的房子与医师的房子相邻；
> 14. 养马的人所住的房子与外交官的房子相邻。

问：

- 哪所房子里的人养斑马
- 哪所房子里的人喝水

按照思路完全可以用穷举法来做:

并且还要选择用最恰当的 数据类型 去描述这个问题，我们是选择用 set, tuple, 还是简单赋值呢?

- 这里需要首先遵循 **保持简练** 的原则，选择最简单的赋值
- 假如在解题过程中碰到不可绕过的错误，再返回这一条然后推倒重来

```
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
	''' 这里使用这种形式的生成器，是为了:
	1. 可以不使用 缩进，方便人类查阅 【难道还有外星人看吗...】
	2. 方便修改，方便调试
结论是：主要为了人类查阅和debug的便利性考虑，当然小伙伴们也是可以写成 缩进+if/else 形式
        的不过那样你的程序就会跑出你的版面，同时要修改及调试也是相对麻烦很多。
	'''
```

我完全没有跑过这段程序，按估算，它至少要跑一小时。

我们来简单做个乘法运算先吧：
> 1. 国籍：     英国、西班牙、日本、意大利、挪威
> 2. 颜色：     红色、绿色、白色、蓝色、黄色
> 3. 工作：     油漆工、摄影师、外交官、小提琴家、医师
> 4. 宠物：     狗、蜗牛、狐狸、马、斑马
> 5. 饮料：     茶、牛奶、咖啡、橘子汁、矿泉水

以上就是条件的汇总，

当仅拿出 **颜色** 来举例，5 所房子，5 种颜色， 就有 5 * 4 * 3 * 2 * 1 = 120 种情况
```
房子A       5 种颜色任选-->(还剩4种颜色)
房子B       4 种颜色任选-->(还剩3种颜色)
房子C       3 种        -->   剩2种
房子D       2 种        -->   剩1种
房子E       1 种
```

并且，同时存在 5 种属性，那么总共有 120 * 120 * 120 * 120 * 120 = 120 ^ 5 = 2.45 * 10^10 种排列式

看到这个数字，再查询下计算机每秒的计算量上限，就可知如果完全遍历这个组合，大概需要跑 **1 Hour** 以上

---

### B. 逻辑优化
接下来就是 穷举法 的**优化精髓**：

我们来重温 #2 (if Englishman == red			#2)， 在这个情况下，

先上代码:

```
import itertools, time

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
	return next((WATER, ZEBRA)
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
```

可以看到，核心就是 **只遍历必须遍历的情况**， 一旦不满足，马上跳至下一条

你优化后的程序只跑了不到1秒...再一次感叹计算机科学的神奇

---

### C. 效率测试
#### C1. 运行时间测试
但是？？究竟跑了多少秒呢？小伙伴们是不是也看到了上面的 import **time** 了？
那么，就让我们展开一系列检测吧...

以下各种迭代版本，让伙伴们先看清一系列优化的改进逻辑

```
def t():
	t0 = time.clock()
	zebra_puzzle_fast()
	t1 = time.clock()
	return t1-t0
''' Beta_1:
	t()只能用来测试 zebra_puzzle_fast() 这单一函数的效率
	我们希望把它扩展成能测试 任何函数 的效率'''

def timedcall(fn, *args):
	# Call function with args; return the time in seconds and result
	t0 = time.clock()
	result = fn(*args)
	t1 = time.clock()
	return t1-t0, result
''' Beta_2:
    此版本能测试 包括带参数的任何函数，但是基于严谨性，
    我们需要一个 测试足够n+次 的 测试函数'''

def timedcalls(n, fn, *args):
	# Call fn(*args) repeatedly: n times if n is an int, or up to
	# n seconds if n is a float; return the min, avg, and max time
	if isinstance(n, int):
		times = [timedcall(fn, *args)[0] for _ in range(n)]
	else:
		times = []
		while sum(times) < n:
			times.append(timedcall(fn, *args)[0])
	return min(times), average(times), max(times)
''' Beta_3:
    既然要采取更多的样本量，首要问题就是决定需要采取 多少 样本量，
    在这个版本里，我们提供两种选择:
        1. 当 n 是 整形 时， 我们采取 n 次样本
        2. 当 n 是 浮点型 时， 我们采取的 样本运行时间总和
        不能超过 n 秒'''

def average(numbers):
	# Retuen the average (arithmetic mean) of a sequence of numbers
	return sum(numbers) / float(len(numbers))
```

---
#### C2. 运行空间测试
测试完 所花费的运行时间 之后，当然要对 运行空间 也要有一个确切的测试

对，我们测试总共 枚举 了多少种 排列数。

对于排列数还不熟悉的可以返回去看 A. 解题方法

当然，测试总不能.........
```
cnt = 0
for (red, green, ivory, yellow, blue) in orderings:
	cnt += 1
	for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in orderings:
		cnt += 1
		for (dog, snails, fox, horse, ZEBRA) in orderings:
			cnt += 1
			for (coffee, tea, milk, oj, WATER) in orderings:
				cnt += 1
				for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in orderings:
					cnt += 1
```

这样吧....
宝宝的心里受到了惊吓....

当解说来到这里之后，我们又进入到了一个大坑，所谓程序设计自然是分好的设计和坏的设计
> 程序设计三大块：
> 1. 业务代码(service_code)
> 2. 效率代码(effi_code)
> 3. 调试代码(debug_code)

```
# 坏的设计
def thisfunction():
    service_code
    effi_code
        service_code
        debug_code
    debug_code
    service_code
        effi_code
        service_code

# 好的设计
def ser_function():
    service_code_1
    service_code_2
        service_coed_3
        service_code_4

def effi_code():
    effi_code_1
    effi_code_2
        efficoed_3

def debug_code():
    debug_code_1
        debug_code_3
    debug_code_2
        debug_code_4
```
其实我也想画图...然而找不到画图的好软件...

好了，基于上面的基础原则，既然我们要 **计算总共枚举了多少排列数**

那我们就把这一段测试代码封装成另几段 测试函数， 给小伙伴们顺便玩个连连看(代码就变成了这样):

```
for (red, ...) in cnt(orderings)
...
for (Englishman, ...) in cnt(orderings)
...
for (coffee, ...) in cnt(orderings)
...
for (OldGold, ...) in cnt(orderings)
...
for (dog, ...) in cnt(orderings)
...
```

```
def instrument_fn(fn, *args):
	cnt.starts, cnt.items = 0, 0
	result = fn(*args)
	print "%s got %s with %5d iters over %7d items" % (
		fn.__name__, result, cnt.starts, cnt.items)

def cnt(sequence):
	""" Generate items in sequence; keeping counts as we go. c.starts is the
	number of sequences; c.items is number of items generated"""
	cnt.starts += 1
	for item in sequence:
		cnt.items += 1
		yield item
```
