import math
from collections import Counter
import time

def stream_data(filename, hashname, countname, functions, buckets):
	counts = open(countname, "r")
	count = {}
	for line in counts:
		numbers = line.strip().split("\t")
		count[int(numbers[0])] = int(numbers[1])
	hashing = open(hashname, "r")
	a, b = [], []
	for line in hashing:
		numbers = line.strip().split("\t")
		a.append(int(numbers[0]))
		b.append(int(numbers[1]))
	hash_1, hash_2, hash_3, hash_4, hash_5 = {}, {}, {}, {}, {}
	hashing = [hash_1, hash_2, hash_3, hash_4, hash_5]
	data = open(filename, "r")
	start_mc = time.clock()
	t = 0
	for line in data:
		number = int(line.strip())
		t += 1
		for i in range(1, 6):
			result = hash_fun(a[i - 1], b[i - 1], 123457, buckets, number)
			if (i, result) not in hashing[i - 1]:
				hashing[i - 1][(i, result)] = 1
			else:
				hashing[i - 1][(i, result)] += 1
	A, B, C, D, E = Counter(hash_1), Counter(hash_2), Counter(hash_3), Counter(hash_4), Counter(hash_5)
	final = dict(A + B + C + D + E)
	print len(final)
	end_mc = time.clock()
	print end_mc - start_mc
	start_mc = time.clock()
	for i in range(1, len(count) + 1):
		min_count = final[(1, hash_fun(a[0], b[0], 123457, buckets, i))]
		for j in range(2, functions + 1):
			if final[(j, hash_fun(a[j - 1], b[j - 1], 123457, buckets, i))] < min_count:
				min_count = final[(j, hash_fun(a[j - 1], b[j - 1], 123457, buckets, i))]
		f_i = count[i]
		error_i = float(min_count - f_i) / f_i
		with open('error.txt', 'a') as writefile:
			writefile.write(str(error_i) + " " + str(float(f_i) / t) + "\n")
	end_mc = time.clock()
	print end_mc - start_mc

def hash_fun(a, b, p, n_buckets, x):
	y = x % p
	hash_val = (a * y + b) % p
	return hash_val % n_buckets

if __name__ == '__main__':
	delta = math.exp(-5)
	epsilon = math.e * 0.0001
	buckets = int(math.ceil(math.e / epsilon))
	functions = int(math.log(1 / delta))
	stream_data("words_stream.txt", "hash_params.txt", "counts.txt", functions, buckets)
