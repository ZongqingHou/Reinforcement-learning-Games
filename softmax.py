import numpy as np
from math import exp
import sys

max_length = 6

def score_func(value):
	return 2 if value % 2 == 0 else 1

def prob_cal(input_dict, index):
	temp = [exp((sum(input_dict[ii]) / len(input_dict[ii]))) for ii in input_dict if len(input_dict[ii]) > 0]
	return exp((sum(input_dict[index]) / (len(input_dict[index])))) /  sum(temp) if len(input_dict[index]) > 0 else exp(0) / sum(temp)

def alph(k, t):
	score = 0
	move_list = {temp:[] for temp in range(1, k + 1)}
	for index in range(t):
		prob = np.random.randn()

		if index == 0:
			value = np.random.randint(1, k + 1)
		else:
			if 0 <= prob <= prob_cal(move_list, 1):
				value = 1
			elif prob_cal(move_list, 1) <= prob <= prob_cal(move_list, 2):
				value = 2

		temp = score_func(value)
		print('you got {}'.format(temp))
		move_list[value].append(temp)
		score += temp
	return score

if __name__ == '__main__':
	np.random.seed(1)
	print(alph(int(sys.argv[1]), int(sys.argv[2])))