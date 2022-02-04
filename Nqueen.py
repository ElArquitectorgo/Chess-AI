# Se han obviado los casos triviales N = 1, 2 y 3

def n_queen(N):
	k = i = 0
	l = [i]
	d = dict()
	cnt = 1
	while k >= 0:
		if len(l) == N:
			if d.get(tuple(l)) == None:
				d[tuple(l)] = cnt
				cnt += 1
			else:
				return d

		while k < N and not is_valid(l, k):
			k += 1
		if k < N:
			l.append(k)
			k = 0
		else:
			if k > N - 1:
				if len(l) == 0:
					i += 1
					l = [i]
				else:
					k = l[-1] + 1
					l.pop()

def is_valid(l, j):
	i = 0
	c = True
	while i < len(l) and c:
		if j == l[i] or len(l) - i == abs(j - l[i]):
			c = False
		i += 1
	return c

d = n_queen(10)
print(len(d))