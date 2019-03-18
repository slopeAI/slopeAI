#adding to AI Library to path
from inspect import getsourcefile
import os.path
import sys
current_path = os.path.abspath(getsourcefile(lambda:0))
current_directory = os.path.dirname(current_path)
parent_directory = current_directory[:current_directory.rfind(os.path.sep)]

sys.path.insert(0, parent_directory)

from AI.sequential import Sequential 
from AI.layers.convolution import *
from AI.layers.activations import *
from AI.layers.hidden import *
from AI.layers.pooling import *
from AI.layers.dropout import Dropout
import AI.learning_rates
import AI.loss
import AI.optimizers
from mnist import  MNIST
import time
import random
import numpy as np

def printIm(img):#prints a representation of the digit
	new_img = [img[i*28:28*(i+1)] for i in range(28)]
	for preLine in img[0]:
		newLine = ["#" if val>0 else "." for val in preLine]
		print(" ".join(newLine))
start_data = time.time()
mndata = MNIST("datasets/digitdata")
images,labels = mndata.load_training()
num_data = 60000# of the 60,000 images in the MNIST database, how many do we want to use
formatted_inputs = []
formatted_labels = []
for ind in range(num_data):
	output = np.zeros(10) 
	output[labels[ind]] = 1
	new_image = np.array([[pxl/255 for pxl in images[ind]]])
	new_image = np.reshape(new_image,(1,28,28))
	formatted_labels.append(output)
	formatted_inputs.append(new_image)
#INITIATING THE MODEL
'''
net = Sequential((784),
				FullyConnected(16),
				Bias(),#
				Sigmoid(),
				FullyConnected(16),
				Bias(),
				Sigmoid(),
				FullyConnected(10),
				Bias(),
				Softmax(),loss = AI.loss.CrossEntropy())
'''
learning_rate = AI.learning_rates.DecayLearningRate(0.1,1)
net = Sequential((1,28,28),
				Convolution2D(num_filters = 32,filter_size = (3,3),stride = (3,3)),
				Bias(),	
				ReLU(),	
				MaxPooling2D(),
				#Dropout(0.5),
				Convolution2D(num_filters = 64, filter_size = (3,3),stride = (3,3)),
				Bias(),
				ReLU(),
				MaxPooling2D(),
				FullyConnected(128),
				Bias(),
				ReLU(),
				#Sigmoid(),
				#Dropout(0.2),
				FullyConnected(10),
				Bias(),
				Softmax(),optimizer = AI.optimizers.BatchGradientDescent(16,momentum = 0.9,learning_rate = learning_rate))
net.open_from_file("builds/digit_identifier/digitweight")# open up from digitweight a pre trained model
num_trials = 2 # how many times we run over the same 10,000 images (epoch)

#TRAINING THE MODEL
score = 0
for i in range(25):
	a = random.randint(0,num_data-1)
	correct = labels[a]
	result = net.run(formatted_inputs[a])
	maxresult = 0
	max_ind = 0
	for ind,val in enumerate(result):
		if val>= maxresult:
			max_ind = ind
			maxresult = val
	maxresult2 = 0
	for ind,layer in enumerate(net.training_run(formatted_inputs[a])[11:]):
		print(net.training_layers[ind+10],layer)
	#printIm(formatted_inputs[a])
	print("ACTUAL,MACHINE:",correct,max_ind,result)
	if correct == max_ind:	
		score+=1
		print('correct')
#print([lyer for lyer in net.weighted_layers])
print("SCORE:",score*4,"TOTAL TIME:",time.time()-start_data)
net.train(formatted_inputs,formatted_labels,epoch = num_trials)#training the mode using stochasatic gradient descent
net.save_from_file("builds/digit_identifier/digitweight")# open up from digitweight a pre trained model
#ASSESING THE MODEL

score = 0
for i in range(100):
	a = random.randint(0,num_data-1)
	correct = labels[a]
	result = net.run(formatted_inputs[a])
	maxresult = 0
	max_ind = 0
	for ind,val in enumerate(result):
		if val>= maxresult:
			max_ind = ind
			maxresult = val
	#for ind,layer in enumerate(net.training_run(formatted_inputs[a])[11:]):
		#print(net.training_layers[ind+10],layer)
	maxresult2 = 0
	#printIm(formatted_inputs[a])
	print("ACTUAL,MACHINE:",correct,max_ind,result)
	if correct == max_ind:	
		score+=1
		print('correct')
#print([lyer for lyer in net.weighted_layers])
print("SCORE:",score,"TOTAL TIME:",time.time()-start_data)