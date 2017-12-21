import pygame, sys, random, time
import numpy as np
import tensorflow as tf
import math

check_errors = pygame.init()
if check_errors[1] > 0:
	print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
	sys.exit(-1)
else:
	print("(+) PyGame successfully initialized!")

playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake game!')

red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

fpsController = pygame.time.Clock()

snakePos = [[100, 50]]
snakeBody = [[100,50], [90,50], [80,50]]

last_snake_pos = snakePos

foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
foodSpawn = True

direction = 'RIGHT'
changeto = direction

score = 0

count_reward = [[0 for index in range(4)]]
direction_index = -1

x = tf.placeholder(tf.float32, [None, 2], name='x-input')
y = tf.placeholder(tf.float32, [None, 4], name='y-check')

changeto_sets = {0: 'UP', 1: 'DOWN', 2: 'LEFT', 3: 'RIGHT'}

with tf.name_scope('snake_game'):
	award_weight1 = tf.get_variable('weight1', [2, 10], initializer=tf.truncated_normal_initializer())
	award_weight2 = tf.get_variable('weight2', [10, 1], initializer=tf.truncated_normal_initializer())
	bias1 = tf.get_variable('bias1', [10], initializer=tf.constant_initializer(1))
	bias2 = tf.get_variable('bias2', [4], initializer=tf.constant_initializer(1))

	temp_y = tf.nn.relu(tf.matmul(x, award_weight1) + bias1)
	y_ = tf.matmul(temp_y, award_weight2) + bias2

loss = tf.reduce_sum(tf.square(y - y_))
train_step = tf.train.AdamOptimizer(0.01).minimize(loss)

def re_init():
	global score
	global snakePos
	global snakeBody
	global direction
	global changeto
	score = 0
	snakePos = [[100, 50]]
	snakeBody = [[100,50], [90,50], [80,50]]
	direction = 'RIGHT'
	changeto = direction

def showScore(choice=1):
	sFont = pygame.font.SysFont('monaco', 24)
	Ssurf = sFont.render('Score : {0}'.format(score) , True, black)
	Srect = Ssurf.get_rect()
	if choice == 1:
		Srect.midtop = (80, 10)
	else:
		Srect.midtop = (360, 120)
	playSurface.blit(Ssurf,Srect)

def softmax(x):
	temp_list = [math.exp(temp - max(x)) for temp in x]
	test_list = [temp / sum(temp_list) for temp in temp_list]
	return test_list.index(max(test_list))

def cal_distance(point1, point2):
	return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

count_award = 0
sess = tf.Session()
tf.global_variables_initializer()

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

		train, out_put = sess.run([train_step, y_], feed_dict={x: snakePos, y: count_reward})

		if changeto == 'RIGHT' and not direction == 'LEFT':
			direction = 'RIGHT'
		if changeto == 'LEFT' and not direction == 'RIGHT':
			direction = 'LEFT'
		if changeto == 'UP' and not direction == 'DOWN':
			direction = 'UP'
		if changeto == 'DOWN' and not direction == 'UP':
			direction = 'DOWN'

		if direction == 'RIGHT':
			direction_index = 3
			snakePos[0][0] += 10
		if direction == 'LEFT':
			direction_index = 2
			snakePos[0][0] -= 10
		if direction == 'UP':
			direction_index = 0
			snakePos[0][1] -= 10
		if direction == 'DOWN':
			direction_index = 1
			snakePos[0][1] += 10

		temp_list = out_put[0].tolist()
		print(temp_list)
		changeto = changeto_sets[softmax(temp_list)]

		snakeBody.insert(0, list(snakePos[0]))
		if snakePos[0][0] == foodPos[0] and snakePos[0][1] == foodPos[1]:
			count_reward[0][direction_index] += 1000
			foodSpawn = False
		else:
			snakeBody.pop()
			
		if foodSpawn == False:
			foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10] 
		foodSpawn = True
	
		playSurface.fill(white)
	
		for pos in snakeBody:
			pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10))
	
		pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0],foodPos[1],10,10))
	
		if cal_distance(snakePos[0], foodPos) < cal_distance(last_snake_pos[0], foodPos):
			count_reward[0][direction_index] += 100
		else:
			count_reward[0][direction_index] -= 50

		if snakePos[0][0] > 710 or snakePos[0][0] < 0:
			count_reward[0][direction_index] -= 1000
			re_init()
			continue
		elif snakePos[0][1] > 450 or snakePos[0][1] < 0:
			count_reward[0][direction_index] -= 1000
			re_init()

		for block in snakeBody[1:]:
			if snakePos[0][0] == block[0] and snakePos[0][1] == block[1]:
				count_reward[0][direction_index] -= 1000
				re_init()

		showScore()
		pygame.display.flip()
		fpsController.tick(60)