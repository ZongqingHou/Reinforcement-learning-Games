import numpy as np

states = ['up', 'down', 'right', 'left']
step_score = {temp: [] for temp in states}
score = 0

def stratgy(snake_pos, snake_body, spawn_pos):
	if snake_pos[0] > snake_body[-1][0]:
		if snake_pos[0] > spawn_pos[0]:
			return 'down'
		elif snake_pos[0] < spawn_pos[1]:
			return 'right'
	elif snake_pos[0] < snake_body[-1][0]:
		if snake_pos[0] > spawn_pos[0]:
			return 'left'
		elif snake_pos[0] < spawn_pos[0]:
			return 'up'
	elif snake_pos[1] > snake_body[-1][1]:
		if snake_pos[1] > spawn_pos[1]:
			return 'left'
		elif snake_pos[1] < spawn_pos[1]:
			return 'up'
	elif snake_pos[1] < snake_body[-1][1]:
		if snake_pos[1] > spawn_pos[1]:
			return 'down'
		elif snake_pos[1] < spawn_pos[1]:
			return 'right'

def calculate_score():
	pass

def evaluate(steps):
	global score
	for index in range(1, steps):
		moved = 0
		# stratgy(snake_pos, snake_body, spawn_pos), stratgy function
		for temp in states:
			step_score[temp].append(calculate_score())
			moved += 1 / (len(states) - 1) * (1 / index * calculate_score() + (t - 1) / t * sum(step_score[temp]))
		score = moved
	return score