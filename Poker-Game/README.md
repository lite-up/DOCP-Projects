# Poker_Game


这几天学习了Udacity上的课程：[DOCP](https://classroom.udacity.com/courses/cs212)，
跟着老师做了个小游戏  **Poker_Game**

上代码，实现是Python

#### 1) 最初构建处理所有手牌hands的函数 Poker()
```
def poker(hands):
	# Return the best hand: poker([hand, ...]) => hand
	return max(hands, key=hand_rank)
```

---

#### 2) 把业务逻辑交给hand_rank()函数，而Poker()只负责返回最大的手牌 hand

核心： 重点是理清hand_rank()的逻辑，它负责判断

```
graph LR
同花顺 --> 四皇
四皇 --> FullHouse
FullHouse --> 同花
同花 --> 顺子
顺子 --> 三张
三张 --> 两对
两对 --> 两张
两张 --> 无任何特点

8-->7
7-->6
6-->5
5-->4
4-->3
3-->2
2-->1
1-->0

```


而hand_rank()返回的 **元组(tuple)** 代表每种手牌的特色，如上图所示

元组内的第一个元素，就是该种类手牌对应的数字，我们来举两个例子：

A
>同花色的 ["6C", "7C", "8C", "9C", TC"]
>
>返回 (手牌对应种类 , 该手牌最大手牌)  --> **(8, 10)**
>
>当我们知道最大手牌是 10 的时候，推导就知道手牌是 (10, 9, 8, 7, 6)，所以没有必要传入整手手牌

B
>同理可得，Full House ["TD", "TC", "TH", "7C", "7D"]
>
>返回 (手牌对应种类 , 手牌内3张相同牌的数值, 手牌内2张相同牌的数值) --> **(6, 10, 7)**

还有一些传入整组手牌的，是根据Python内 **>/<(比较大小操作符)** 对元组的操作顺序而决定的。

主要是针对 **平局** 时候的判定结果
```
def hand_rank(hands):
	# Return a value indicating the ranking of a hand
	ranks = card_rank(hands)
	if staright(ranks) and flush(ranks):
		return (8, max(ranks))
	elif kind(4, ranks):
		return (7, kind(4, ranks), kind(1, ranks))
	elif kind(3, ranks) and kind(2, ranks):
		return (6, kind(3, ranks), kind(2, ranks))
	elif flush(ranks):
		return (5, ranks)
	elif straight(ranks):
		return (4, max(ranks))
	elif kind(3, ranks):
		return (3, kind(3, ranks), ranks)
	elif two_pair(ranks):
		return (2, two_pair(ranks), ranks)
	elif kind(2, ranks):
		return (1, kind(2, ranks), ranks)
	else:
		return (0, ranks)
```

---

#### 3) card_ranks() 输入一组手牌，返回该手牌从大到小的 排序列表

这里我们是摒弃了花色之后再进行的排序
>同花色的 ["6C", "7C", "8C", "9C", TC"]
>
>返回 [10, 9, 8, 7, 6]
并且考虑到极端值 Ace > King, 所以'--23456789TJQKA'内没有 1， 取而代之的是把 A 放在了最高位
```
def card_ranks(hand):
	# Return a list of the ranks, sorted with higher first
	ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
	ranks.sort(reverse=True)
	return ranks
```

---

#### 4) staright() 和 flush() 判断是否顺子，判断是否同花
这里最初我是遍历了所有ranks内所有元素的大小，并且进行了比较

然后当我看到老师的解法的时候....再一次感叹Program的神奇
```
def straight(ranks):
	# Return True if the ordered ranks form a 5-card straight
	return len(set(ranks)) == 5 and (max(ranks)-min(ranks) == 4)

def flush(hand):
	# Return True if all the cards have the same suit
	suits = [s for r, s in hand]
	return len(set(suits)) == 1
```
---

#### 5) kind() 判断一组手牌内有无 n 张同样的手牌
利用Python build-in 函数 count() 完成了这个功能
```
def kind(n, ranks):
	# Return the first rank that this hand has exactly n of
	# Return None if there is no n-of-a-kind in the hand.
	for r in ranks:
		if ranks.count(r) == n:
			return r
	return None
```
---
#### 6) two_pair() 判断一组手牌内有无 两对对子
这里我应用了 staright() 函数的判断方式， 但老师的解法是另外一种
```
def two_pair(ranks):
	# If there are two pair, return the the two ranks as a
	# tuple: (highest, lowest); otherwise return None
	if len(set(ranks)) == 3 and len(ranks) == 5:
		pair = kind(2, ranks)
		lowpair = kind(2, ranks[2:])
		return (pair, lowpair)
	return None
```
老师的解法:
```
def two_pair(ranks):
        pair = kind(2, ranks)
        low_pair = kind(2, list(reversed(ranks)))
        if pair and lowpair != pair:
            return (pair, lowpair)
        else:
            return None
```
我也不知道哪个更好点，不过我觉得我的也蛮靠谱的...

---

#### 7) 测试函数test(), 测试上述所有函数是否构建完全：
可以在这里看到上述所有例子的测试
```
def test()
	# Test cases for the functions in poker program
	sf = "6C 7C 8C 9C TC".split()	# straight flush
	fk = "9D 9H 9S 9C 7D".split()	# four of a king
	fh = "TD TC TH 7C 7D".split()	# full house
	tp = "5S 5D 9H 9C 6S".split()	# two pair
	s1 = "AS 2S 3S 4S 5C".split()	# A-5 straight
	s2 = "2C 3C 4C 5S 6S".split()	# 2-6 straight
	ah = "AS 2S 3S 4S 6C".split()	# A high
	sh = "2S 3S 4S 6C 7D".split()	# 7 hight

	assert poker([s1, s2, ah, sh]) == s2

	fkranks = card_ranks(fk)
	tpranks = card_ranks(tp)

	assert kind(4, fkranks) == 9
	assert kind(3, fkranks) == None
	assert kind(2, fkranks) == None
	assert kind(1, fkranks) == 7
	assert two_pair(fkranks) == None
	assert two_pair(tpranks) == (9, 5)

	assert straight([9, 8, 7, 6, 5]) == True
	assert straight([9, 8, 8, 6, 5]) == False
	assert flush(sf) == True
	assert flush(fk) == False

	assert poker([sf, fk, fh]) == sf
	assert poker([fk, fh]) == fk
	assert poker([fh, fh]) == fh
	assert poker([sf]) == sf
	assert poker([sf] + 99*[fh]) == sf

	assert hand_rank(sf) == (8, 10)
	assert hand_rank(fk) == (7, 9, 7)
	assert hand_rank(fh) == (6, 10, 7)

	assert card_ranks(sf) == [10, 9, 8, 7, 6]
	assert card_ranks(fk) == [9, 9, 9, 9, 7]
	assert card_ranks(fh) == [10, 10, 10, 7, 7]

	return "tests pass"
```

---

嗯，暂且是这么多，以后还有更多的要改进呢 = =

See you~
