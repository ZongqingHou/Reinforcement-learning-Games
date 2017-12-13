import numpy as np
import sys

max_length = 6

def score_func(value):
	return 2 if value % 2 == 0 else -1

def alph(k, t, prob):
	score = 0
	move_list = {temp:[] for temp in range(k)}
	for index in range(t):
		if np.random.randn() < prob:
			value = np.random.randint(1, k)
		else:
			value = np.argmax([sum(move_list[temp]) / len(move_list[temp]) for temp in move_list if len(move_list[temp]) != 0])

		temp = score_func(value)
		print('you got {}'.format(temp))
		move_list[value].append(temp)
		score += temp
	return score

if __name__ == '__main__':
	np.random.seed(1)
	prob = np.random.randn()
	print(alph(int(sys.argv[1]), int(sys.argv[2]), prob))