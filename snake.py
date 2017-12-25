import pygame, sys, random, time, math

import numpy as np
import tensorflow as tf
import os.path

WIDTH = 100
LENGTH = 100

MODEL_DIR = "model/ckpt"
MODEL_NAME = "model.ckpt"

# color sets
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

controller = pygame.time.Clock()

snake_pos = [50, 50]
snake_body = [[50, 50], [40, 50], [30, 50]]

temp_snake_pos = snake_pos

food_pos = [random.randrange(1,10)*10,random.randrange(1,10)*10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

change_to_sets = {0: 'UP', 1:'DOWN', 2:'LEFT', 3:'RIGHT'}
score = 0

count_award = {}
direction_index = -1

state_input = tf.placeholder(tf.float32, [None, 2], name='input')
previous_award = tf.placeholder(tf.float32, [None, 4], name='check')

with tf.name_scope('snake_game'):
	state_weight = tf.get_variable('state_weight', [2, WIDTH * LENGTH], initializer=tf.truncated_normal_initializer())
	action_weight = tf.get_variable('action_weight', [WIDTH * LENGTH, 4], initializer=tf.truncated_normal_initializer())
	bias = tf.get_variable('bias', [WIDTH * LENGTH], initializer=tf.constant_initializer(6))

def re_init():
	global score
	global snake_pos
	global snake_body
	global direction
	global change_to
	score = 0
	snake_pos = [50, 50]
	snake_body = [[50,50]]
	direction = 'RIGHT'
	change_to = direction

def showScore(choice=1):
	sFont = pygame.font.SysFont('monaco', 24)
	Ssurf = sFont.render('Score : {0}'.format(score) , True, black)
	Srect = Ssurf.get_rect()
	if choice == 1:
		Srect.midtop = (0, 10)
	else:
		Srect.midtop = (50, 50)
	user_interface.blit(Ssurf,Srect)

def softmax(input_list):
	temp_list = [math.exp(temp - max(input_list)) for temp in input_list]
	result_list = [temp / sum(temp_list) for temp in temp_list]
	return result_list.index(max(result_list))

def cal_distance(point1, point2):
	return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

check_errors = pygame.init()
if check_errors[1] > 0:
	print('error {} occur...').format(check_errors[1])
	sys.exit(-1)
else:
	print('lets rock and roll the world!')

user_interface = pygame.display.set_mode((LENGTH, WIDTH))

temp_y = tf.nn.relu(tf.matmul(state_input, state_weight) + bias)
y_ = tf.matmul(temp_y, action_weight)
loss = tf.reduce_sum(tf.square(previous_award - y_))
train_op = tf.train.AdamOptimizer(0.001).minimize(loss)

if not tf.gfile.Exists(MODEL_DIR):
    tf.gfile.MakeDirs(MODEL_DIR)

saver = tf.train.Saver()

with tf.Session() as sess:
	tf.global_variables_initializer().run()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.event.post(pygame.event.Event(pygame.QUIT))

		temp_input = [snake_pos]
		award_index = str(snake_pos[0]) + ',' + str(snake_pos[1])

		if not award_index in count_award:
			count_award[award_index] = [[0 for index in range(4)]]

		train, out_put = sess.run([train_op, y_], feed_dict={state_input: temp_input, previous_award: count_award[award_index]})
		print(out_put[0])
		change_to = change_to_sets[softmax(out_put[0])]

		saver.save(sess, os.path.join(MODEL_DIR, MODEL_NAME))

		if change_to == 'RIGHT' and not direction == 'LEFT':
			direction = 'RIGHT'
			direction_index = 3
		if change_to == 'LEFT' and not direction == 'RIGHT':
			direction = 'LEFT'
			direction_index = 2
		if change_to == 'UP' and not direction == 'DOWN':
			direction = 'UP'
			direction_index = 0
		if change_to == 'DOWN' and not direction == 'UP':
			direction = 'DOWN'
			direction_index = 1

		if direction == 'RIGHT':
			snake_pos[0] += 10
		if direction == 'LEFT':
			snake_pos[0] -= 10
		if direction == 'UP':
			snake_pos[1] -= 10
		if direction == 'DOWN':
			snake_pos[1] += 10

		snake_body.insert(0, list(snake_pos))
		if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
			count_award[award_index][0][direction_index] += 1000
			food_spawn = False
		else:
			snake_body.pop()
			
		if food_spawn == False:
			food_pos = [random.randrange(1,10)*10,random.randrange(1,10)*10] 
		food_spawn = True
	
		user_interface.fill(white)
	
		for pos in snake_body:
			pygame.draw.rect(user_interface, green, pygame.Rect(pos[0],pos[1],10,10))
	
		pygame.draw.rect(user_interface, brown, pygame.Rect(food_pos[0],food_pos[1],10,10))
	
		if cal_distance(snake_pos, food_pos) < cal_distance(temp_snake_pos, food_pos):
			count_award[award_index][0][direction_index] += 100
		else:
			count_award[award_index][0][direction_index] -= 50

		temp_snake_pos = snake_pos

		if snake_pos[0] > 90 or snake_pos[0] < 0:
			count_award[award_index][0][direction_index] -= 1000
			re_init()
			continue
		elif snake_pos[1] > 90 or snake_pos[1] < 0:
			count_award[award_index][0][direction_index] -= 1000
			re_init()
			continue

		for block in snake_body[1:]:
			if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
				count_award[award_index][0][direction_index] -= 1000
				re_init()

		showScore()
		pygame.display.flip()
		controller.tick(60)