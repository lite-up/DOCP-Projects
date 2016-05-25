# 用Python解决 覆面算 问题
这次的问题本质上是解决一个 覆面算(我也不懂这个中文什么意思) 公式

**ABC + ABC == DEFG**

我们要把公式里的 **字母** 替换成对应的 **数字**，并返回使得这个公式正确的 **数字 结果**

问题就是这样，接下来我们遵循解决Zebra_puzzle的步骤，来解决这个问题

---
## A. **Concept Inventory**

首先有 两种等式:

1. original:    has letters
2. filled:      has digits

--> 可以推理得出

**letters, digits** 就是我们需要提纯的概念，并且由于是等式。

**assignment, set** 赋值和集合也是需要考虑的范围

最后还有 **evaluation(估算)** 这个概念

---

## B. **Refine ideas**

我们把上述所建立的 概念仓库 转换成一张 表格，则有：

CONCEPT | | | REPRESENTATION 
---|---|---|---
equations |  |  |
 - | original (letters) | --> | str 'D'
 - | fill_in (digits)  | --> | str '3'
assignment |  |  |
 - | letters->digit | --> | table 'D' -> '3'、str.translate()
evaluation |  | --> | build-in: eval()

---
## C1. code LOGIC
```
import string

table = string.maketrans('ABC', '123')
formula = 'A + B == C'
fill_in = f.translate(table) --> '1 + 2 == 3'

finally:
    eval(fill_in) --> True
```
---

但是，由于eval只判断算式的 True or False，而我们想要能够检测出别的算数错误

例如
- 除0运算 /0
- 不同进制间运算
- 浮点数运算

废话不多说，上代码:
### C1_1. valid()
```
from __future__ import division

def valid(formula):
	# Formula f is valid iff it has no numbers with leading zero, and evals true.
	try:
		return not re.search(r'\b0[0-9]', formula) and eval(formula) is True
	except ArithmeticError:
		return False
		
'''
    re.search(r'\b0[0-9]', f)
    b for boundary, 是匹配'XXX + YYY = 0ZZZ'即以 0开头并处于算式尾端 的数字
    由于C语言的历史遗留问题，python会将0开头的数字解析成 八进制
    很明显是不符合我们的 十进制 运算
    
    __future__模块引入Python 3.0 的出发特性，使得浮点数运算更加精确
    Py2             Py3
    3/2 = 1         3/2 = 1.5
    1/2 = 0         1/2 = 0.5
'''
```
这就排除了上述的两种错误种类：
~~- 除0运算 /0~~
~~- 不同进制间运算~~
~~-浮点数运算~~

### C1_2. solve()
```
def solve(formula):
	""" Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it
	Input formula is a string; output is a digit-filled-in string or None"""
	for eachfor in fill_in(formula):
		if valid(eachfor):
			return eachfor
			
'''
    这个函数与上一个函数的逻辑关联非常强
    同时也引申出下一个关键函数fill_in()，暂时写不出来没关系
    因为我也是照抄的~
'''
```

---

## C2. code LOGIC #2
我们再来看看C1的那段伪代码
```
import string

table = string.maketrans('ABC', '123')
formula = 'A + B == C'
fill_in = f.translate(table) --> '1 + 2 == 3'

finally:
    eval(fill_in) --> True
```

会发现，C1的 valid()和solve()都是 **finally:** 那块的具体代码

也就是说finally以上的代码，我们都会封装进 **fill_in()** 里面

### C2_1. fill_in()
```
def fill_in(formula):
	# Generate all possible fillings-in of letters in formula with digits
	letters = ''.join(set(re.findall('[A-Z]', formula)))
	for digits in itertools.permutations('1234567890', len(letters)):
		table = string.maketrans(letters, ''.join(digits))
		yield formula.translate(table)
		
'''
    itertools.permutations()我们在zebra_puzzle里面是见过的，它返回某列表的所有排列集合
    permutations([1, 2, 3]) = [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 2, 1), (3, 1, 2)]
    而传入第二个参数是什么意思呢？ 请自己Google...
    
    这段代码的逻辑是：
    1. 找出算式中的所有非重复大写字母:  'ODD + ODD == EVEN' --> [O, D, E, V, E, N]
    2. len([O, D..., N]) = 6, 则选出6个非重复数字分别匹配它们
    3. 映射
    4. 生成
'''
```

最后献上测试函数：
```
examples = """TWO + TWO == FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**2.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3 + RM**3 == N**3 + RX**3
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANETS])""".splitlines()

def test():
	t0 = time.clock()
	for example in examples:
		print; print 13*' ', example
		print '%6.4f sec:   %s ' % timedcall(solve, example)
	print '%6.4f tot.' % (time.clock() - t0)
```

![image](http://imglf.nosdn.127.net/img/dHhnQUpIRjlOdTJDdUJMWjJQL2xTcUt2eDRLMWlpZ1B6N0Qvdlllc253aU9XYk9GWC95RlRRPT0.png?imageView&thumbnail=1680x0&quality=96&stripmeta=0&type=jpg)

---
持续更新~~~