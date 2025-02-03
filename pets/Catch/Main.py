import pygame
import sys
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1" #for linux

import random
import math

import time
import displayio
from adafruit_display_shapes.rect import Rect
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# Initialize Pygame
display = PyGameDisplay(width=128, height=128)

splash = displayio.Group()
display.show(splash)

pygame.init()
# screen = pygame.display.set_mode((128, 128))
# clock = pygame.time.Clock()
# pygame.display.set_caption('HackDogs')
running = True

# background1 = pygame.image.load(os.path.join(art_dir, "FetchBG.png")).convert_alpha()
# dog = pygame.image.load(os.path.join(art_dir, "dog1_0.png")).convert_alpha()
# ball = pygame.image.load(os.path.join(art_dir, "Ball.png")).convert_alpha()

# background1 = pygame.transform.scale(background1, (128, 128))
# dog = pygame.transform.smoothscale(dog, (15, 15))
# ball = pygame.transform.scale(ball, (3, 3))
# ballHealth = pygame.transform.scale(ball, (10, 10))
background = displayio.OnDiskBitmap("./art/FetchBG.png")
background_sprite = displayio.TileGrid(
	background,
	pixel_shader=background.pixel_shader,
	x=0,
	y=0,
)
splash.append(background_sprite)

# Load dog sprite
dog_sheet = displayio.OnDiskBitmap("./art/Dog.png")
dog_sprite = displayio.TileGrid(
	dog_sheet,
	pixel_shader=dog_sheet.pixel_shader,
	width=1,
	height=1,
	tile_width=32,
	tile_height=32,
	x=(display.width - 32) // 2,
	y=display.height - 32 - 10,
)
splash.append(dog_sprite)

# Load ball sprite
ball_sheet = displayio.OnDiskBitmap("./art/Ball.png")
ball_sprite = displayio.TileGrid(
	ball_sheet,
	pixel_shader=ball_sheet.pixel_shader,
	width=1,
	height=1,
	tile_width=32,
	tile_height=32,
	x=(display.width - 32) // 2,
	y=display.height - 32 - 10,
)
splash.append(ball_sprite)

# text
font = bitmap_font.load_font("./art/Arial-12.bdf")
score_label = label.Label(font, text="Score: 0", color=0x000000)
score_label.x = 10
score_label.y = 10
splash.append(score_label)
highscore_label = label.Label(font, text="Highscore: 0", color=0x000000)
highscore_label.x = 10
highscore_label.y = 25
splash.append(highscore_label)
ballsLeft_label = label.Label(font, text="Balls Left: 3", color=0x000000)
ballsLeft_label.x = 10
ballsLeft_label.y = 40
splash.append(ballsLeft_label)
# screen = pygame.display.set_mode((128, 128))

dog_sprite.x, dog_sprite.y = 50, 50
dogTarget = [50, 50]
dogSpeed = 1

def rgb_to_hex(r, g, b):
	return (r << 16) | (g << 8) | b

ballTarget = [64, 64]
mode = 1 # 1 = up, 2 = down, 3 = left, 4 = right
ballTargetSpeed = 5
numberOfSteps = 1
numberOfSquares = 0
drawnPath = False
pathSquares = []
def clear_path():
	global drawnPath, pathSquares
	if pathSquares:
		for square in pathSquares[:]:  # Iterate over copy to avoid modification during iteration
			try:
				splash.remove(square)
			except ValueError:
				pass  # Skip if square already removed
		pathSquares.clear()
		drawnPath = False
def DrawThrowPath(ballTarget):
	global numberOfSteps, numberOfSquares, drawnPath, pathSquares

	clear_path()

	initSize = 4
	NumSquares = int(math.sqrt((ballTarget[0] - 64)**2 + (ballTarget[1] - 128)**2) / initSize)
	numberOfSteps = NumSquares
	startPos = [64, 120]
	distancex = ballTarget[0] - startPos[0]
	distancey = ballTarget[1] - startPos[1]

	if NumSquares <= 1:
		NumSquares = 2
	stepx = distancex / (NumSquares - 1)
	stepy = distancey / (NumSquares - 1)

	for i in range(1, NumSquares):
		x = int(startPos[0] + i * stepx)
		# y = startPos[1] + i * stepy
		y = int(startPos[1] + i * stepy - 25 * math.sin(math.pi * i / (NumSquares - 1)))
		squareSize = int((y / initSize)/10)
		if squareSize < 1:
			squareSize = 1
		# print(squareSize)
		colorSubtract = 255 - int((i / NumSquares) * 255)
		# hexColor = rgb_to_hex(255, colorSubtract, colorSubtract)
		# pygame.draw.rect(screen, (255-colorSubtract, 255-colorSubtract, 255-colorSubtract), (x, y, squareSize, squareSize))
		# Rect(80, 20, 41, 41, fill=0x0)
		# Rect(x, y, squareSize, squareSize, fill=0x0)
		# splash.pop(Rect()))
		rgb = (255-colorSubtract, 255-colorSubtract, 255-colorSubtract)
		color_int = rgb_to_hex(*rgb)
		square = Rect(x, y, squareSize, squareSize, fill=color_int)
		pathSquares.append(square)
		splash.append(square)
	numberOfSquares = NumSquares
	drawnPath = True

	# if not thrownBall:
	# 	for i in range(numberOfSquares):
	# 		# splash.pop()
	# 		print("popped")
	# print(NumSquares)

ballSpeed = 2
debugpath = []
def distanceAlongLine(x1, y1, x2, y2, x, y): # xy: point 1, x1y2: overlap point, x2y2: point 2
	PA = ((x - x1)**2 + (y - y1)**2)**0.5
	AB = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
	# print(PA/AB)
	return PA / AB
def throwBall(clock, pos, target):
	global thrownBall, roundOver, score, ballsLeft

	roundOver = False
	clockTime = 1

	if clock >= clockTime:
		initSize = 4
		NumSquares = int(math.sqrt((target[0] - 64)**2 + (target[1] - 128)**2) / initSize)
		if NumSquares <= 1:
			NumSquares = 2

		startPos = [64+13, 120+13]  # Match DrawThrowPath offset
		distancex = target[0] - startPos[0]
		distancey = target[1] - startPos[1]

		stepx = distancex / (NumSquares - 1)
		stepy = distancey / (NumSquares - 1)

		i = clock
		new_x = int(startPos[0] + i * stepx)
		new_y = int(startPos[1] + i * stepy - 25 * math.sin(math.pi * i / (NumSquares - 1)))
		
		animationSpeed = .01
		clock += animationSpeed

		if clock >= NumSquares:
			clock = 0
			thrownBall = False
			distance = math.sqrt((dog_sprite.x - ball_sprite.x) ** 2 + (dog_sprite.y - ball_sprite.y) ** 2)
			if distance <= 10:
				score += 1
				print("Caught ball!")
			else:
				ballsLeft -= 1
				print("Missed ball!")
		
		debugpath.append((new_x, new_y))
		ball_sprite.x = new_x - 13  # Remove offset for sprite position
		ball_sprite.y = new_y - 13
		# return (new_x, new_y)
	else:
		# return pos
		pass

current_frame = 0
dogAnimationTimer = 0
isDogMoving = False
def moveDog(target):
	global isDogMoving, dogAnimationTimer

	# Unpack positions - target includes +13 offset already
	target_x, target_y = target
	current_x, current_y = dog_sprite.x, dog_sprite.y  # Remove +13 offset here

	# Movement settings 
	speed = 2.0
	FRAME_DELAY = 5

	# Calculate direction and distance
	dx = (target_x - 13) - current_x  # Remove offset from target
	dy = (target_y - 13) - current_y
	distance = math.sqrt(dx**2 + dy**2)

	# If not at target, move dog
	if distance > speed:
		isDogMoving = True

		# Calculate movement vector
		move_x = (dx / distance) * speed
		move_y = (dy / distance) * speed
		
		# Apply movement
		new_x = current_x + move_x
		new_y = current_y + move_y
		
		# Clamp to screen bounds
		dog_sprite.x = max(0, min(128, int(new_x)))
		dog_sprite.y = max(0, min(128, int(new_y)))

		# Update sprite animation
		dogAnimationTimer += 1
		if dogAnimationTimer >= FRAME_DELAY:
			dogAnimationTimer = 0

		# Set sprite direction based on movement
		if abs(dx) > abs(dy):
			dog_sprite[0] = 0 if dx > 0 else 2  # right/left
		else:
			dog_sprite[0] = 1 if dy > 0 else 3  # down/up
	else:
		isDogMoving = False
		dogAnimationTimer = 0
		isDogMoving = False
		# if returningBall:
		# 	catchBallCheck()

isReturning = False
isDogMoving = False
def catchBallCheck():
	global thrownBall, isReturning, roundOver, isDogMoving, score

	START_POS = 50, 120
	radius = 4

	if not isReturning:
		# Check if close enough to catch ball
		dx = ball_sprite.x - dog_sprite.x
		dy = ball_sprite.y - dog_sprite.y
		distance = math.sqrt(dx**2 + dy**2)

		if distance < radius:
			isReturning = True
			# Start return journey
			moveDog(START_POS)
			isDogMoving = True
	else:
		# During return journey
		ball_sprite.x, ball_sprite.y = dog_sprite.x, dog_sprite.y  # Ball follows dog
		roundOver = True
		isDogMoving = False

		# Check if reached start position
		dx = START_POS[0] - dog_sprite.x
		dy = START_POS[1] - dog_sprite.y
		distance = math.sqrt(dx**2 + dy**2)

		if distance < 20:
			# Reset everything
			print("Ball returned!")
			dog_sprite.x, dog_sprite.y = 59, 115
			ball_sprite.x, ball_sprite.y = START_POS[0], START_POS[1]
			thrownBall = False
			isReturning = False
			roundOver = False

		else:
			# Keep moving to start
			moveDog(START_POS)

def scale_sprite(sprite, scale_factor):
	# pass
	# sprite.transform = displayio.MatrixTransformation(scale=scale_factor)
	splash.remove(sprite)
	sprite.scale = .001
	cords = sprite.x, sprite.y
	splash.append(sprite)
	sprite.x, sprite.y = cords
	return sprite

# Main game loop
# cooldowns
modeChangeCooldown = 0 # prevent unwanted switching
thrownBall = False
BallClock = 0 # for animation
ball_sprite.x, ball_sprite.y = 59, 120
calcDistance = True
ballsLeft = 3
score = 0
highscore = 0
roundOver = False
gameOver = False
while running:
	# clock.tick(10)
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
		pass
		dogTarget = [random.randint(10, 128 - 20), random.randint(54, 100 - 20)]
	if thrownBall and not isReturning:
		dogTarget = ballTarget
	if not isReturning:
		moveDog(dogTarget)
	# if not isReturning and roundOver and isDogMoving:
	# 	# check to see how close the dog is to the ball
	# 	distance = math.sqrt((dog_sprite.x - ball_sprite.x)**2 + (dog_sprite.y - ball_sprite.y)**2)
	# 	if distance >= 20:
	# 		ballsLeft -= 1
	# 		# score -= 2
	# 		print("lost ball")
	# 	elif distance <= 19:
	# 		score += 1
	# 		print("caught ball")
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
		dog_sprite.x, dog_sprite.y = 50, 50
		dogTarget = [50, 50]
		ballTarget = [64, 64]
		modeChangeCooldown = 0
		ball_sprite.x, ball_sprite.y = 59, 120
		calcDistance = True
		isDogMoving = False
		dogAnimationTimer = 0
		BallClock = 0


	catchBallCheck()

	# pos clampers
	# dog_sprite.x = max(0, min(128 - dog.get_width(), dog_sprite.x))
	# dog_sprite.y = max(0, min(128 - dog.get_height(), dog_sprite.y))

	# ballTarget[0] = max(0, min(128 - ball.get_width(), ballTarget[0]))
	# ballTarget[1] = max(0, min(128 - ball.get_height(), ballTarget[1]))


	# Scale the dog proportionally based on its position
	dog_scale_factor = dog_sprite.y / 64
	ball_scale_factor = ball_sprite.y / 64

	if dog_scale_factor != 1:
		# splash.remove(dog_sprite)
		dog_sprite.scale = 6
		# dog_sprite = scale_sprite(dog_sprite, dog_scale_factor)
		dog_sprite = scale_sprite(dog_sprite, dog_scale_factor)
		# splash.append(dog_sprite)

	if ball_scale_factor != 1:
		# splash.remove(ball_sprite)
		# ball_sprite = scale_sprite(ball_sprite, ball_scale_factor)
		ball_sprite = scale_sprite(ball_sprite, ball_scale_factor)
		# splash.append(ball_sprite)
	# dog_scaled = pygame.transform.scale(dog, (int(dog.get_width() * dog_scale_factor), int(dog.get_height() * dog_scale_factor)))
	# ball_scaled = pygame.transform.scale(ball, (int(ball.get_width() * ball_scale_factor), int(ball.get_height() * ball_scale_factor)))

	# screen.blit(background1, (0, 0))
	# screen.blit(dog_scaled, dogPos)
	ballsLeft_label.text = f"Balls Left: {ballsLeft}"

	if thrownBall:
		BallClock += 1
		if calcDistance:
			distancex = ballTarget[0] - ball_sprite.x
			distancey = ballTarget[1] - ball_sprite.y
			distance = math.sqrt(distancex**2 + distancey**2)
			distancex /= distance
			distancey /= distance
			calcDistance = False
		throwBall(BallClock, (ball_sprite.x, ball_sprite.y), ballTarget)
	# screen.blit(ball_scaled, ballPos)

	if not thrownBall:
		BallClock = 0
		DrawThrowPath(ballTarget)
	# debug
	# if demoScaleFactor != 1:
		# debug1 = font.render(f"DogTarget {dogTarget[0]}, {dogTarget[1]}", True, (0, 0, 0))
		# screen.blit(debug1, (10, 10))
		# debug2 = font.render(f"DogPos {dog_sprite.x}, {dog_sprite.y}", True, (0, 0, 0))
		# screen.blit(debug2, (10, 30))
		# debug3 = font.render(f"mode {mode}, {modeChangeCooldown}", True, (0, 0, 0))
		# screen.blit(debug3, (10, 50))
		# debug4 = font.render(f"Extra {not isReturning} {not roundOver} {isDogMoving}", True, (0, 0, 0))
		# screen.blit(debug4, (10, 70))

		# debugpath
		# for pos in debugpath:
		# 	pygame.draw.rect(screen, (255, 0, 0), (pos[0], pos[1], 2, 2))
	# screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 50))
	# screen.blit(font.render(f"Highscore: {highscore}", True, (0, 0, 0)), (10, 70))

	if throwBall:
		drawnPath = False

	score_label.text = f"Score: {score}"
	highscore_label.text = f"Highscore: {highscore}"

	# print(dog_sprite.width, dog_sprite.height, dog_scale_factor)
	# time.sleep(.05)
	# print(isReturning)
	# put small red square on dog
	# splash.append(Rect(dog_sprite.x+13, dog_sprite.y+13, 2, 2, fill=0xFF0000))
	# put small yellow square on ball
	# splash.append(Rect(ball_sprite.x+13, ball_sprite.y+13, 2, 2, fill=0xFFFF00))
	time.sleep(.05)

	# pygame.display.flip()