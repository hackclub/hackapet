import pygame
import sys
import os
import random
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((128, 128))
clock = pygame.time.Clock()
pygame.display.set_caption('HackDogs')
running = True
font = pygame.font.Font(None, 36)

base_dir = os.path.dirname(__file__)
art_dir = os.path.join(base_dir, "./art")

background1 = pygame.image.load(os.path.join(art_dir, "FetchBG.png")).convert_alpha()
dog = pygame.image.load(os.path.join(art_dir, "dog1_0.png")).convert_alpha()
ball = pygame.image.load(os.path.join(art_dir, "Ball.png")).convert_alpha()

demoScaleFactor = 5
background1 = pygame.transform.scale(background1, (128*demoScaleFactor, 128*demoScaleFactor))
dog = pygame.transform.smoothscale(dog, (15*demoScaleFactor, 15*demoScaleFactor))
ball = pygame.transform.scale(ball, (3*demoScaleFactor, 3*demoScaleFactor))
ballHealth = pygame.transform.scale(ball, (10*demoScaleFactor, 10*demoScaleFactor))

screen = pygame.display.set_mode((128*demoScaleFactor, 128*demoScaleFactor))

dogPos = [50*demoScaleFactor, 50*demoScaleFactor]
dogTarget = [50*demoScaleFactor, 50*demoScaleFactor]
dogSpeed = 1

ballTarget = [64*demoScaleFactor, 64*demoScaleFactor]
mode = 1 # 1 = up, 2 = down, 3 = left, 4 = right
ballTargetSpeed = 5
numberOfSteps = 1
def DrawThrowPath(ballTarget):
	global numberOfSteps

	initSize = 1*demoScaleFactor
	NumSquares = int(math.sqrt((ballTarget[0] - 64*demoScaleFactor)**2 + (ballTarget[1] - 128*demoScaleFactor)**2) / (initSize * demoScaleFactor))
	numberOfSteps = NumSquares
	startPos = [64*demoScaleFactor, 120*demoScaleFactor]
	distancex = ballTarget[0] - startPos[0]
	distancey = ballTarget[1] - startPos[1]

	if NumSquares <= 1:
		NumSquares = 2
	stepx = distancex / (NumSquares - 1)
	stepy = distancey / (NumSquares - 1)

	for i in range(1, NumSquares):
		x = startPos[0] + i * stepx
		# y = startPos[1] + i * stepy
		y = startPos[1] + i * stepy - 100 * math.sin(math.pi * i / (NumSquares - 1))
		squareSize = (y / initSize)/10
		# print(squareSize)
		colorSubtract = 255 - int((i / NumSquares) * 255)
		pygame.draw.rect(screen, (255-colorSubtract, 255-colorSubtract, 255-colorSubtract), (x, y, squareSize, squareSize))
import math

ballSpeed = 2 * demoScaleFactor
debugpath = []
def distanceAlongLine(x1, y1, x2, y2, x, y): # xy: point 1, x1y2: overlap point, x2y2: point 2
	PA = ((x - x1)**2 + (y - y1)**2)**0.5
	AB = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
	# print(PA/AB)
	return PA / AB
def throwBall(clock, pos, target):
	global thrownBall, roundOver, score, dogPos

	roundOver = False
	clockTime = 1

	if clock >= clockTime:
		x, y = pos
		target_x, target_y = target
		ogX, ogY = (59 * demoScaleFactor, 120 * demoScaleFactor)

		# steps for smoother animation
		NumSquares = 100
		step_x = (target_x - ogX) / NumSquares
		step_y = (target_y - ogY) / NumSquares

		animationSpeed = 0.00000001

		i = clock
		new_x = ogX + i * step_x
		new_y = ogY + i * step_y - 100 * math.sin(math.pi * i / (NumSquares - 1))

		clock += animationSpeed
		if clock >= NumSquares:
			clock = 0
			thrownBall = False
			distance = math.sqrt((dogPos[0] - dogPos[0]) ** 2 + (dogPos[1] - dogPos[1]) ** 2)
			if distance >= 5*demoScaleFactor:
				score += 1

		# add small red box to debugpath
		debugpath.append((new_x, new_y))

		return (new_x, new_y)
	else:
		return pos

current_frame = 0
dogAnimationTimer = 0
isDogMoving = False
def moveDog(target, pos):
	global dogPos, isDogMoving, dogAnimationTimer, dog

	# Unpack positions
	target_x, target_y = target
	current_x, current_y = pos

	# Movement settings
	speed = 2.0
	FRAME_DELAY = 5

	# Calculate direction and distance
	dx = target_x - current_x
	dy = target_y - current_y
	distance = math.sqrt(dx**2 + dy**2)

	# If not at target, move dog
	if distance > speed:
		isDogMoving = True
		# Calculate new position
		dx = (dx / distance) * speed
		dy = (dy / distance) * speed
		dogPos = [current_x + dx, current_y + dy]

		# Update sprite animation
		dogAnimationTimer += 1
		if dogAnimationTimer >= FRAME_DELAY:
			dogAnimationTimer = 0

		# Set sprite direction
				# Determine dominant direction based on absolute values
		if abs(dx) > abs(dy):
			# Horizontal movement dominant
			if dx > 0:  # right
				dog = pygame.image.load(os.path.join(art_dir, "dog1_0.png")).convert_alpha()
			else:  # left
				dog = pygame.image.load(os.path.join(art_dir, "dog1_2.png")).convert_alpha()
		else:
			# Vertical movement dominant
			if dy > 0:  # down
				dog = pygame.image.load(os.path.join(art_dir, "dog1_1.png")).convert_alpha()
			else:  # up
				dog = pygame.image.load(os.path.join(art_dir, "dog1_3.png")).convert_alpha()
	else:
		# At target
		dogAnimationTimer = 0
		isDogMoving = False
		# if returningBall:
		# 	catchBallCheck()

isReturning = False
isDogMoving = False
def catchBallCheck():
	global thrownBall, ballPos, dogPos, isReturning, roundOver, isDogMoving, score

	START_POS = (59 * demoScaleFactor, 120 * demoScaleFactor)
	radius = 1 * demoScaleFactor

	if not isReturning:
		# Check if close enough to catch ball
		dx = ballPos[0] - dogPos[0]
		dy = ballPos[1] - dogPos[1]
		distance = math.sqrt(dx**2 + dy**2)

		if distance < radius:
			isReturning = True
			# Start return journey
			moveDog(START_POS, dogPos)
			isDogMoving = True
	else:
		# During return journey
		ballPos = dogPos  # Ball follows dog
		roundOver = True
		isDogMoving = False

		# Check if reached start position
		dx = START_POS[0] - dogPos[0]
		dy = START_POS[1] - dogPos[1]
		distance = math.sqrt(dx**2 + dy**2)

		if distance < radius:
			# Reset everything
			dogPos = [59*demoScaleFactor, 115*demoScaleFactor]
			ballPos = START_POS
			thrownBall = False
			isReturning = False
			score += 1

		else:
			# Keep moving to start
			moveDog(START_POS, dogPos)

# Main game loop
# cooldowns
modeChangeCooldown = 0 # prevent unwanted switching
thrownBall = False
BallClock = 0 # for animation
ballPos = (59*demoScaleFactor, 120*demoScaleFactor)
calcDistance = True
ballsLeft = 3
score = 0
highscore = 0
roundOver = False
gameOver = False
while running:
	clock.tick(10*demoScaleFactor)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# cooldowns
	if modeChangeCooldown < 10:
		modeChangeCooldown += 1
	# Get keys pressed
	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP] and keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
		# print("throw")
		thrownBall = True
	if keys[pygame.K_LEFT] and not thrownBall:
		if mode == 1:
			ballTarget[0] -= ballTargetSpeed
		if mode == 2:
			ballTarget[1] += ballTargetSpeed
	if keys[pygame.K_RIGHT] and not thrownBall:
		if mode == 1:
			ballTarget[0] += ballTargetSpeed
		if mode == 2:
			ballTarget[1] -= ballTargetSpeed
	if keys[pygame.K_UP] and not thrownBall:
		if modeChangeCooldown >= 10:
			if mode == 2:
				mode = 1
			else:
				mode += 1
			modeChangeCooldown = 0

	if not isDogMoving and not thrownBall and not isReturning:
		dogTarget = [random.randint(0, 128*demoScaleFactor - dog.get_width()), random.randint(54*demoScaleFactor, 100*demoScaleFactor - dog.get_height())]
	if thrownBall and not isReturning:
		dogTarget = ballTarget
	if not isReturning:
		moveDog(dogTarget, (dogPos[0], dogPos[1]))
	if not isReturning and not roundOver and isDogMoving:
		# check to see how close the dog is to the ball
		distance = math.sqrt((dogPos[0] - ballPos[0])**2 + (dogPos[1] - ballPos[1])**2)
		if distance <= 1*demoScaleFactor:
			ballsLeft -= 1
			score -= 2
	if not isReturning and not roundOver and isDogMoving:
		distance = math.sqrt((dogPos[0] - ballPos[0])**2 + (dogPos[1] - ballPos[1])**2)
		if distance <= 1*demoScaleFactor:
			score += 1
	if ballsLeft == 0:
		# game over
		gameOver = True
		if score > highscore:
			highscore = score
		score = 0
		ballsLeft = 3
		isReturning = False
		thrownBall = False
		roundOver = False
		dogPos = [50*demoScaleFactor, 50*demoScaleFactor]
		dogTarget = [50*demoScaleFactor, 50*demoScaleFactor]
		ballTarget = [64*demoScaleFactor, 64*demoScaleFactor]
		modeChangeCooldown = 0
		ballPos = (59*demoScaleFactor, 120*demoScaleFactor)
		calcDistance = True
		isDogMoving = False
		dogAnimationTimer = 0
		BallClock = 0


	catchBallCheck()

	# pos clampers
	dogPos[0] = max(0, min(128*demoScaleFactor - dog.get_width(), dogPos[0]))
	dogPos[1] = max(0, min(128*demoScaleFactor - dog.get_height(), dogPos[1]))

	ballTarget[0] = max(0, min(128*demoScaleFactor - ball.get_width(), ballTarget[0]))
	ballTarget[1] = max(0, min(128*demoScaleFactor - ball.get_height(), ballTarget[1]))


	# Scale the dog proportionally based on its position
	dog_scale_factor = dogPos[1] / (64 * demoScaleFactor)
	ball_scale_factor = ballPos[1] / (64 * demoScaleFactor)
	dog_scaled = pygame.transform.scale(dog, (int(dog.get_width() * dog_scale_factor), int(dog.get_height() * dog_scale_factor)))
	ball_scaled = pygame.transform.scale(ball, (int(ball.get_width() * ball_scale_factor), int(ball.get_height() * ball_scale_factor)))

	screen.blit(background1, (0, 0))
	screen.blit(dog_scaled, dogPos)
	if ballsLeft >= 1:
		screen.blit(ballHealth, (60*demoScaleFactor, 5*demoScaleFactor))
	if ballsLeft >= 2:
		screen.blit(ballHealth, (80*demoScaleFactor, 5*demoScaleFactor))
	if ballsLeft >= 3:
		screen.blit(ballHealth, (100*demoScaleFactor, 5*demoScaleFactor))

	if thrownBall:
		BallClock += 1
		if calcDistance:
			distancex = ballTarget[0] - ballPos[0]
			distancey = ballTarget[1] - ballPos[1]
			distance = math.sqrt(distancex**2 + distancey**2)
			distancex /= distance
			distancey /= distance
			calcDistance = False
		ballPos = throwBall(BallClock, ballPos, ballTarget)
	screen.blit(ball_scaled, ballPos)

	if not thrownBall:
		BallClock = 0
		DrawThrowPath(ballTarget)
	# debug
	if demoScaleFactor != 1:
		debug1 = font.render(f"DogTarget {dogTarget[0]}, {dogTarget[1]}", True, (0, 0, 0))
		# screen.blit(debug1, (10, 10))
		debug2 = font.render(f"DogPos {dogPos[0]}, {dogPos[1]}", True, (0, 0, 0))
		# screen.blit(debug2, (10, 30))
		debug3 = font.render(f"mode {mode}, {modeChangeCooldown}", True, (0, 0, 0))
		# screen.blit(debug3, (10, 50))
		debug4 = font.render(f"Extra {not isReturning} {not roundOver} {isDogMoving}", True, (0, 0, 0))
		# screen.blit(debug4, (10, 70))

		# debugpath
		# for pos in debugpath:
		# 	pygame.draw.rect(screen, (255, 0, 0), (pos[0], pos[1], 2*demoScaleFactor, 2*demoScaleFactor))
	screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 50))
	screen.blit(font.render(f"Highscore: {highscore}", True, (0, 0, 0)), (10, 70))


	pygame.display.flip()