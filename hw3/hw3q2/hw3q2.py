import numpy
import math
import time
import random
from collections import defaultdict
from operator import itemgetter

def initialize_matrix(filename, n):
	# intialize M to zeros
	matrix = []
	for i in range(n):
		matrix.append([0 for j in range(n)])

	# store all outgoing edges in a multimap
	node_map = defaultdict(list)
	f = open(filename, 'r')
	for line in f:
		edge = line.strip().split("\t")
		node_map[int(edge[0])].append(int(edge[1]))

	f1 = open(filename, 'r')
	for line in f1:
		nodes = line.strip().split("\t")
		matrix[int(nodes[1]) - 1][int(nodes[0]) - 1] = 1.0/len(node_map[int(nodes[0])])
	return numpy.matrix(matrix), node_map

def power_iteration(matrix, r, n, beta):
	vector_one = numpy.matrix([1 for i in range(n)]).transpose()
	r = (1 - beta) / n * vector_one + beta * matrix * r
	return r
	
def mc_algorithm(matrix, n, beta, node_map, R):
	all_path = []
	for k in range(R):
		for i in range(1, 101):
			path = [i]
			while True:
				number = random.random()
				if number < (1 - beta):
					break
				else:
					choices = len(node_map[path[-1]])
					number2 = int(random.random() * choices)
					path.append(node_map[path[-1]][number2])
			all_path += path
	r_tilde = [float(all_path.count(i)) / ((n * R) / (1 - beta)) for i in range(1, 101)]
	return numpy.matrix(r_tilde).transpose()

if __name__ == '__main__':
	n, beta = 100, 0.8
	R = 5
	K = 10
	matrix, node_map = initialize_matrix("graph.txt", n)
	# initialize pagerank vector
	r = numpy.matrix([1.0/n for i in range(n)]).transpose()
	start = time.clock()
	for i in range(40):
		r = power_iteration(matrix, r, n, beta)
	end = time.clock()
	print end - start

	start_mc = time.clock()
	r_tilde = mc_algorithm(matrix, n, beta, node_map, R)
	end_mc = time.clock()
	print end_mc - start_mc

	r_list = numpy.array(r.T)[0].tolist()
	r_sorted = sorted(r, key = itemgetter(0), reverse = True)
	topk_index = []
	for i in range(K):
		topk_index.append(r_list.index(r_sorted[i]))

	r_simulate = mc_algorithm(matrix, n, beta, node_map, R)
	r_simulate_list = numpy.array(r_simulate.T)[0].tolist()
	
	# compute average absolute error
	error = 0
	for i in range(100):
		absolute_error = 0
		r_simulate = mc_algorithm(matrix, n, beta, node_map, R)
		r_simulate_list = numpy.array(r_simulate.T)[0].tolist()
		for j in topk_index:
			absolute_error += math.fabs((numpy.array(r_simulate_list) - numpy.array(r_list))[j])
		error += (1.0 / K) * absolute_error
	print error / 100
