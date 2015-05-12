import random
import numpy

def readFile(filename, k):
	trainingSet = open(filename, 'r')
	maxUserID, maxMovieID = 0, 0
	for line in trainingSet:
		ratings = line.strip().split("\t")
		# determine the dimensions of p and q
		if int(ratings[0]) > maxUserID:
			maxUserID = int(ratings[0])
		if int(ratings[1]) > maxMovieID:
			maxMovieID = int(ratings[1])

	# initialization of p and q
	pvector, qvector= ['dummy'], ['dummy']
	for i in xrange(maxUserID):
		line = [(float(5)/k)**0.5*random.random() for i in range(k)]
		pvector.append(line)

	for i in xrange(maxMovieID):
		line = [(float(5)/k)**0.5*random.random() for i in range(k)]
		qvector.append(line)
	
	return pvector, qvector

def new_readFile(filename, k):
	trainingSet = open(filename, 'r')
	maxUserID, maxMovieID, totalRating, counter = 0, 0, 0, 0
	for line in trainingSet:
		ratings = line.strip().split("\t")
		totalRating += int(ratings[2])
		counter += 1
		# determine the dimensions of p and q
		if int(ratings[0]) > maxUserID:
			maxUserID = int(ratings[0])
		if int(ratings[1]) > maxMovieID:
			maxMovieID = int(ratings[1])

	# initialization of p, q, b_x and b_i
	pvector, qvector, bxvector, bivector = ['dummy'], ['dummy'], ['dummy'], ['dummy']
	for i in xrange(maxUserID):
		line1 = [(float(5)/k)**0.5*random.random() for i in range(k)]
		pvector.append(line1)
		line2 = (float(5)/k)**0.5*random.random()
		bxvector.append(line2)

	for i in xrange(maxMovieID):
		line3 = [(float(5)/k)**0.5*random.random() for i in range(k)]
		qvector.append(line3)
		line4 = (float(5)/k)**0.5*random.random()
		bivector.append(line4)

	return pvector, qvector, bxvector, bivector, float(totalRating) / counter

# update the equations
def update(filename, pvector, qvector, k, lamda):
	learningRate = 0.025
	inputFile = open(filename, 'r')
	for line in inputFile:
		ratings = line.strip().split("\t")
		userID, movieID, rating = int(ratings[0]), int(ratings[1]), int(ratings[2])
		epilson_iu = rating - numpy.dot(qvector[movieID], pvector[userID])
		qi_update, pu_update = [], []
		for i in range(k):
			qi_update.append(qvector[movieID][i] + learningRate * (epilson_iu * pvector[userID][i] - lamda * qvector[movieID][i]))
			pu_update.append(pvector[userID][i] + learningRate * (epilson_iu * qvector[movieID][i] - lamda * pvector[userID][i]))
			
		qvector[movieID], pvector[userID] = qi_update, pu_update

	return pvector, qvector

def new_update(filename, pvector, qvector, bxvector, bivector, mean, k, lamda):
	learningRate1 = 0.1
	learningRate2 = 0.01
	inputFile = open(filename, 'r')
	for line in inputFile:
		ratings = line.strip().split("\t")
		userID, movieID, rating = int(ratings[0]), int(ratings[1]), int(ratings[2])
		epilson_iu = rating - numpy.dot(qvector[movieID], pvector[userID]) - bxvector[userID] - bivector[movieID] - mean
		qi_update, pu_update = [], []
		for i in range(k):
			qi_update.append(qvector[movieID][i] + learningRate1 * (epilson_iu * pvector[userID][i] - lamda * qvector[movieID][i]))
			pu_update.append(pvector[userID][i] + learningRate1 * (epilson_iu * qvector[movieID][i] - lamda * pvector[userID][i]))

		qvector[movieID], pvector[userID] = qi_update, pu_update
		bivector[movieID] += learningRate2 * (numpy.dot(qvector[movieID], pvector[userID]) - lamda * bivector[movieID]) 
		bxvector[userID] += learningRate2 * (numpy.dot(qvector[movieID], pvector[userID]) - lamda * bxvector[userID])

	return pvector, qvector, bxvector, bivector

# calculate the E function
def calculate_error(filename, pvector, qvector, lamda):
	input_file = open(filename, 'r')
	error = 0
	for line in input_file:
		ratings = line.strip().split("\t")
		userID, movieID, rating = int(ratings[0]), int(ratings[1]), int(ratings[2])
		pu_l2norm = numpy.linalg.norm(pvector[userID])
		qi_l2norm = numpy.linalg.norm(qvector[movieID])
		error += (rating - numpy.dot(qvector[movieID], pvector[userID])) ** 2
	# add the squares of L2 norms into the error 
	error += lamda * (pu_l2norm ** 2 + qi_l2norm ** 2)
	return error

def new_calculate_error(filename, pvector, qvector, bxvector, bivector, mean, lamda):
	input_file = open(filename, 'r')
	error = 0
	for line in input_file:
		ratings = line.strip().split("\t")
		userID, movieID, rating = int(ratings[0]), int(ratings[1]), int(ratings[2])
		error += (rating - numpy.dot(qvector[movieID], pvector[userID]) - bxvector[userID] - bivector[movieID] - mean) ** 2
		pu_l2norm = numpy.linalg.norm(pvector[userID])
		qi_l2norm = numpy.linalg.norm(qvector[movieID])
		bx_l2norm = numpy.linalg.norm(bxvector[userID])
		bi_l2norm = numpy.linalg.norm(bivector[movieID])

	error += lamda * (pu_l2norm ** 2 + qi_l2norm ** 2 + bx_l2norm ** 2 + bi_l2norm ** 2)
	return error

# calculate traning and test error
def calculate_trainingtesterror(filename, pvector, qvector):
	input_file = open(filename, 'r')
	error = 0
	for line in input_file:
		ratings = line.strip().split("\t")
		userID, movieID, rating = int(ratings[0]), int(ratings[1]), int(ratings[2])
		error += (rating - numpy.dot(qvector[movieID], pvector[userID])) ** 2

	return error

def new_calculate_trainingtesterror(filename, pvector, qvector, bxvector, bivector, mean):
	input_file = open(filename, 'r')
	error = 0
	for line in input_file:
		ratings = line.strip().split("\t")
		userID, movieID, rating = int(ratings[0]), int(ratings[1]), int(ratings[2])
		error += (rating - numpy.dot(qvector[movieID], pvector[userID]) - bxvector[userID] - bivector[movieID] - mean) ** 2

	return error

if __name__ == '__main__':
	k = 20
	lamda = 0
	iteration = 40
	# calculate error E when k = 20, lambda = 0.2
	pvector, qvector = readFile("ratings.train.txt", k)
	for i in range(iteration):
		pvector, qvector = update("ratings.train.txt", pvector, qvector, k, lamda)
		error = calculate_error("ratings.train.txt", pvector, qvector, lamda)
		with open("ratings.error.txt", 'a') as write_file:
			write_file.write(str(error) + '\n')

	write_file.close()

	# calculate training and test error when for k = 1 to 10 and lambda = 0 or 0.2
	for i in range(1, 11):
		pvector, qvector = readFile("ratings.train.txt", i)
		for j in range(iteration):
			pvector, qvector = update("ratings.train.txt", pvector, qvector, i, lamda)
		
		train_error = calculate_trainingtesterror("ratings.train.txt", pvector, qvector)
		test_error = calculate_trainingtesterror("ratings.val.txt", pvector, qvector)

		with open("smallerlambda.txt", 'a') as write_file1:
			write_file1.write(str(train_error) + ' ' + str(test_error) + '\n')

	write_file1.close()

	# calculate new training error E when k = 20, lambda = 0.2
	pvector, qvector, bxvector, bivector, mean = new_readFile("ratings.train.txt", k)
	for i in range(iteration):
		pvector, qvector, bxvector, bivector = new_update("ratings.train.txt", pvector, qvector, bxvector, bivector, mean, k, lamda)
		error = new_calculate_error("ratings.train.txt", pvector, qvector, bxvector, bivector, mean, lamda)

		with open("ratings.newerror.txt", 'a') as write_file2:
			write_file2.write(str(error) + '\n')

	write_file2.close()

	# calculate new training and test error when for k = 1 to 10 and lambda = 0 or 0.2
	for i in range(1, 11):
		pvector, qvector, bxvector, bivector, mean = new_readFile("ratings.train.txt", i)
		for j in range(iteration):
			pvector, qvector, bxvector, bivector = new_update("ratings.train.txt", pvector, qvector, bxvector, bivector, mean, i, lamda)
		
		train_error = new_calculate_trainingtesterror("ratings.train.txt", pvector, qvector, bxvector, bivector, mean)
		test_error = new_calculate_trainingtesterror("ratings.val.txt", pvector, qvector, bxvector, bivector, mean)

		with open("newsmallerlambda.txt", 'a') as write_file3:
			write_file3.write(str(train_error) + ' ' + str(test_error) + '\n')

	write_file3.close()