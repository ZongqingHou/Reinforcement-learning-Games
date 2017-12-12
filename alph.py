import numpy as np
import sys

max_length = 6

def score_func(value):
	return 2 if value % 2 == 0 else -1


def alph(k, t, prob):
	score = 0
	move_list = [0 for temp in range(k)]
	for index in range(t):
		if np.random.randn() < prob:
			value = np.random.randint(1, k)
		else:
			value = np.argmax(move_list)

		temp = score_func(value)
		print('you got {}'.format(temp))
		score += temp
		move_list[value] = (sum(move_list) + temp) / (len(move_list) + 1)
	return score

if __name__ == '__main__':
	np.random.seed(16)
	prob = np.random.randn()
	print(alph(int(sys.argv[1]), int(sys.argv[2]), prob))