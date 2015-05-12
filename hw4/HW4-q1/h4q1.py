import math	
import numpy	
import time

def batch_gradient_descent(filenamex, filenamey, C, eta, epsilon, n):
	k = 0
	b = 0
	w_0 = [0.0 for i in range(122)]
	y = []
	target = open(filenamey, "r")
	for line in target:
		y.append(int(line.strip()))
	features = open(filenamex, "r")
	x = []
	for line in features:
		feature = line.strip().split(",")
		thisline = []
		for f in feature:
			thisline.append(int(f))
		x.append(thisline)
	while True:
		fk_before = calculate_convergence(w_0, b, x, y, C, n)
		with open('bgd.txt', 'a') as write_file:
			write_file.write(str(fk_before) + ' ' + str(k) + '\n')
		matrix = multiplication(w_0, b, x, y, n)
		for j in range(len(w_0)):
			w_update = w_0
			sigma_l = 0
			for i in range(n):
				if matrix[i] != 0:
					sigma_l += -y[i] * x[i][j]
			gradient_wb = w_0[j] + C * sigma_l
			w_update[j] = w_0[j] - eta * gradient_wb
		w_0 = w_update
		sigma_l_b = 0
		for i in range(n):
			if matrix[i] != 0: 
				sigma_l_b += -y[i]
		b -= eta * C * sigma_l_b
		k += 1
		print k
		fk_after = calculate_convergence(w_0, b, x, y, C, n)
		print math.fabs(fk_after - fk_before) * 100 / fk_before, fk_after
		if math.fabs(fk_after - fk_before) * 100 / fk_before < epsilon:
			with open('bgd.txt', 'a') as write_file:
				write_file.write(str(fk_after) + ' ' + str(k) + '\n')
			break
	return w_0, b

def stochastic_gradient_descent(filenamex, filenamey, C, eta, epsilon, n):
	i = 1 
	k = 0
	b = 0
	cost = 0
	w_0 = [0.0 for m in range(122)]
	y = []
	target = open(filenamey, "r")
	for line in target:
		y.append(int(line.strip()))
	features = open(filenamex, "r")
	x = []
	for line in features:
		feature = line.strip().split(",")
		thisline = []
		for f in feature:
			thisline.append(int(f))
		x.append(thisline)
	for m in range(n):
		x[m].append(y[m])
	numpy.random.shuffle(x)
	for m in range(n):
		y[m] = x[m][-1]
		del x[m][-1] 
	while True:
		fk_before = calculate_convergence(w_0, b, x, y, C, n)
		with open('sgd.txt', 'a') as write_file:
			write_file.write(str(fk_before) + ' ' + str(k) + '\n')
		matrix = multiplication(w_0, b, x, y, n)
		for j in range(len(w_0)):
			w_update = w_0
			l = 0
			if matrix[i - 1] != 0:
				l += -y[i - 1] * x[i - 1][j]
			gradient_wb = w_0[j] + C * l
			w_update[j] = w_0[j] - eta * gradient_wb
		w_0 = w_update
		l_b = 0
		if matrix[i - 1] != 0:
			l_b += -y[i - 1]
		b -= eta * C * l_b
		i = i % n + 1
		k += 1
		print k
		fk_after = calculate_convergence(w_0, b, x, y, C, n)
		cost = 0.5 * cost + 0.5 * math.fabs(fk_after - fk_before) * 100 / fk_before 
		print cost, fk_after
		if cost < epsilon:
			with open('sgd.txt', 'a') as write_file:
				write_file.write(str(fk_after) + ' ' + str(k) + '\n')
			break
	return w_0, b

def minibatch_gradient_descent(filenamex, filenamey, C, eta, epsilon, n):
	k = 0
	b = 0
	l = 0
	cost = 0 
	batch_size = 20
	w_0 = [0.0 for m in range(122)]
	y = []
	target = open(filenamey, "r")
	for line in target:
		y.append(int(line.strip()))
	features = open(filenamex, "r")
	x = []
	for line in features:
		feature = line.strip().split(",")
		thisline = []
		for f in feature:
			thisline.append(int(f))
		x.append(thisline)
	for m in range(n):
		x[m].append(y[m])
	numpy.random.shuffle(x)
	for m in range(n):
		y[m] = x[m][-1]
		del x[m][-1]
	while True:
		fk_before = calculate_convergence(w_0, b, x, y, C, n)
		with open('mbgd.txt', 'a') as write_file:
			write_file.write(str(fk_before) + ' ' + str(k) + '\n')
		matrix = multiplication(w_0, b, x, y, n)
		for j in range(len(w_0)):
			w_update = w_0
			sigma_L = 0
			for i in range(l * batch_size, min(n, (l + 1) * batch_size)):
				if matrix[i] != 0:
					sigma_L += -y[i] * x[i][j]
			gradient_wb = w_0[j] + C * sigma_L
			w_update[j] = w_0[j] - eta * gradient_wb
		w_0 = w_update
		l_b = 0
		for i in range(l * batch_size, min(n, (l + 1) * batch_size)):
			if matrix[i] != 0: 
				l_b += -y[i]
		b -= eta * C * l_b
		l = (l + 1) % ((n + batch_size - 1) / batch_size)
		k += 1 
		print k
		fk_after = calculate_convergence(w_0, b, x, y, C, n)
		cost = 0.5 * cost + 0.5 * math.fabs(fk_after - fk_before) * 100 / fk_before
		print cost, fk_after
		if cost < epsilon:
			with open('mbgd.txt', 'a') as write_file:
				write_file.write(str(fk_after) + ' ' + str(k) + '\n')
			break

def	multiplication(w_0, b, x, y, n): 
	matrix = [0 for i in range(n)] 
	for i in range(n):
		if y[i] * (numpy.dot(x[i], w_0) + b) < 1:
			matrix[i] = 1
	return matrix	

def	calculate_convergence(w_0, b, x, y, C, n):	
	sigma_max = 0	
	for i in range(n):	
		sigma_wx = 0
		for j in range(len(w_0)):
			sigma_wx += w_0[j] * x[i][j]
		if y[i] * (sigma_wx + b) < 1:
			sigma_max += 1 - y[i] * (sigma_wx + b)
	sigma_w = 0
	for j in range(len(w_0)):
		sigma_w += math.pow(w_0[j],2)
	return 0.5 * sigma_w + C * sigma_max

def calculate_error(w_0, b, filenamex, filenamey):
	y = []
	target = open(filenamey, "r")
	for line in target: 
		y.append(int(line.strip())) 
	features = open(filenamex, "r") 
	prediction = []
	for line in features:
		feature = line.strip().split(",")
		sigma_wx = 0
		index = 0
		for x in feature:
			sigma_wx += int(x) * w_0[index]
			index += 1
		if sigma_wx + b > 0:
			prediction.append(1)
		else:
			prediction.append(-1)
	error = 0.0
	for i in range(len(y)):
		if prediction[i] != y[i]:
			error += 1
	return error / len(y)
 
if __name__ == "__main__": 
	C = 100
	eta = 0.0001 
	epsilon = 0.001
	start_mc = time.clock()
	batch_gradient_descent("features.txt", "target.txt", C, 0.0000003, 0.25, 6414)
	stochastic_gradient_descent("features.txt", "target.txt", C, 0.0001, 0.001, 6414)
	minibatch_gradient_descent("features.txt", "target.txt", C, 0.00001, 0.01, 6414)
	values = [1, 10, 50, 100, 200, 300, 400, 500]
	for val in values:
		w_0, b = stochastic_gradient_descent("features.train.txt", "target.train.txt", val, eta, epsilon, 6000)
		error = calculate_error(w_0, b, "features.test.txt", "target.test.txt")
		print error
		with open('error.txt', 'a') as write_file:
			write_file.write(str(error) + ' ' + str(val) + '\n')
	end_mc = time.clock()
	print end_mc - start_mc
