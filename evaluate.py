import numpy as np
import copy

states = []
action = []

action_pro = []
state_pro = []
temp = 0

def calculate(temp_action, temp_state):
	pass

for step in (1, steps):
	temp_move = 0
	for temp_action in range(len(action)):
		for temp_state in range(len(states)):
			temp_reward = calculate(temp_action, temp_state)
			temp_move += action_pro[temp_action] * state_pro[temp_state] * (1 / steps * temp_reward + (step - 1) / step * (temp + temp_reward))


	temp = temp_move

