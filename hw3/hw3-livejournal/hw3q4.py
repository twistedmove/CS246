# store all nodes in a set
def readfile(filename):
	nodes = set()
	lines = open(filename, 'r')
	for line in lines:
		node = line.strip().split("\t")
		nodes.add(int(node[0]))
		nodes.add(int(node[1]))
	return nodes

def find_dense_subgraph(filename, nodes, epsilon):
	s_tilde = nodes
	s = nodes
	counter = 0
	while len(s) != 0:
		counter += 1
		s = removenodes(nodes, filename, s, epsilon)
		dense, e_c = density(s, nodes)
		dense_tilde, e_c_tilde = density(s_tilde, nodes)
		'''if epsilon != 0.05:
			with open("q4c1.txt", 'a') as write_file:
				write_file.write(str(counter) + ' ' + str(dense) + ' ' + str(e_c) + ' ' + str(len(s)) + '\n')
		else:
			with open("q4c2.txt", 'a') as write_file:
				write_file.write(str(counter) + ' ' + str(dense) + ' ' + str(e_c) + ' ' + str(len(s)) + '\n')'''
		# since density of an empty set is zero, s_tilde is not updated
		if len(s) == 0:
			break
		elif dense > dense_tilde:
			s_tilde = s
	return s_tilde, dense_tilde, e_c_tilde, len(s_tilde)

def removenodes(nodes, filename, s, epsilon):
	s_copy = s.copy()
	dense, e_s = density(s, nodes)
	degree = calculate_degree(filename, s, nodes)
	for i in s:
		if degree[i] <= 2 * (1 + epsilon) * dense:
			s_copy.remove(i)
	return s_copy
		
def calculate_degree(filename, s, nodes):
	degreelines = open(filename, 'r')
	degree = initialize_degree(nodes)
	for line in degreelines:
		edge = line.strip().split("\t")
		if int(edge[0]) in s and int(edge[1]) in s:
			degree[int(edge[0])] += 1
			degree[int(edge[1])] += 1
	return degree

def initialize_degree(nodes):
	degree = {}
	for node in nodes:
		degree[node] = 0
	return degree

def density(s, nodes):
	nodelines = open(filename, 'r')
	e_s = 0
	for line in nodelines:
		node = line.strip().split("\t")
		if int(node[0]) in s and int(node[1]) in s:
			e_s += 1
	if e_s == 0:
		return 0, 0
	else:
		return e_s * 1.0 / len(s), e_s


if __name__ == '__main__':
	filename = "livejournal-undirected.txt"
	epsilons = [0.1, 0.5, 1, 2, 0.05]
	nodes = readfile(filename)
	'''for i in range(5):
		find_dense_subgraph(filename, nodes, epsilons[i])'''
	epsilon = 0.05
	for i in range(20):
		s_tilde, lo, E, cardinality = find_dense_subgraph(filename, nodes, epsilon)
		nodes_copy = nodes.copy()
		for node in nodes:
			if node in s_tilde:
				nodes_copy.remove(node)
		nodes = nodes_copy
		with open("q4c3.txt", 'a') as write_file:
			write_file.write(str(lo) + ' ' + str(E) + ' ' + str(cardinality) + '\n')
	
