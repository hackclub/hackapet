import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import random

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

background = displayio.OnDiskBitmap("bgl.bmp")

bg_sprite = displayio.TileGrid(
	background, 
	pixel_shader=background.pixel_shader,
	x=0,
	y=-128
)

# add the ferris sprite here:
ferris_sheet = displayio.OnDiskBitmap("ferris-sheet.bmp")

ferris_sprite = displayio.TileGrid(
	ferris_sheet,
	pixel_shader=ferris_sheet.pixel_shader,
	width=1,
	height=1,
	tile_width=64,
	tile_height=64,
	default_tile=0,
	x=32,
	y=54
)
ferris_sprite[0] = 3

frame = 0
dialoge = 1
question = None
lives = 3
life_progress = 0

ferris_dialoge = [
	"Hello,\nI'm Ferris!",
	("I usually live\nin a terminal", 1),
	"But right now\nIm on vacation!",
	"The problem is\nall the users",
	"keep aksing me\nto debug code",
	"So I cant\nrelax at all!",
	("...", 0),
	("Say, do you\nknow Rust?", 3),
	"You can learn\non the job!",
	"What job?",
	"Youre going to\ndebug for me!",
	("It's pretty\nsimple...", 1),
	("Just spot\nthe bad code!",2),
	"And select it",
	"Ooh, perfect\ntiming!",
	("File Incoming!",	0),
	0,
	1,
	2,
	3,
	("it looks like\n you got it!", 2),
	"more or less\n...",
	"I'll be taking\na nap",
	(32, -64),
	("...", 8),
	(32, 54),
	"zzz...",
	4,
	5,
	6,
	7,
	8, 
	9, 
	10,
	("How's it going\nover there?", 1),
	"Oh! you're\nstill here?",
	"Most people\nleave by now",
	("Impressive!", 2),
	"Let's keep\nit up!",
	"I'm going to\nget some coffee",
	(-64, 54),
	11,
	12, 
	13, 
	14,
	15,
	16,
	("Hey, I'm back!", 4),
	(32, 54),
	"Did you miss me?",
	"Of course you\n did", 
	"That was a\nshort file",
	"I wonder \nwhat's next?",
	("...", 0),
	("Uh oh, this\ncode is tricky", 1),
	"Let's see if\nyou can get it",
	"lifetimes\ncan be tough",
	17,
	18,
	("We're almost\nthere!", 2),
	"I can see the\nend!",
	"Look out, \nPointers!",
	19,
	20,
	21,
	"Those were\ntough ones",
	("I see the last\none coming up!", 3),
	("oh...", 1),
	"oh no...",
	("oh no no no...", 6),
	"oh no no no\nno...",
	("oh no no no\nno no...", 7),
	("OH GOODNESS\nGRAVIOUS!", 5),
	"THIS IS\nNOT GOOD!",
	"GOOD LUCK!",
	(128, 54),
	"LET ME KNOW\nONCE IT'S OVER",
	22,
	("oh, well, um\n", 1),
	(32, 54),
	("that's it!", 3),
	"thanks for\nthe help!",
	"that was...\nalmost relaxing",
]

questions = [
	{
		"options": ["print(\"a\");", "print!(\"a\");"],
		"correct": 0
	},
	{
		"options": ["a = 4", "let a = 4;"],
		"correct": 0,
	},
	{
		"options": ["fn foo(){}", "fn (foo) {}"],
		"correct": 1,
	},
	{
        "options": ["fn main(){}", "fn main()"],
        "correct": 1,
	},
	{
		"options": ["let a: i32 = '4'","let a: i32 = 4"],
		"correct": 0,
	},
	{
		"options": ["for i in 0..10 {\n println!(\"{}\", i)}", "for i in 0..10 {\n println!(i)}"],
		"correct": 0
	},
	{
		"options": ["let mut x = 5;\nx=2", "let x = 5;\nx=2"],
		"correct": 1
	},
	{
		"options": ["let x: int = 5;", "let x: i32 = 5;"],
		"correct": 0
	},
	{
		"options": ["let mut y = 5;\n&y = 3", "let mut y = 5;\ny=3"],
		"correct": 0
	},
	{
		"options": ["let x = \"hello\";", "let x = 'hello';"],
		"correct": 1
	},
	{

		"options": ["let x = [1, 2, 3];", "let x = {1, 2, 3};"],
		"correct": 1
	},
	#11-16
	{
		"options": ["let x = 5;", "let x == 5"],
		"correct": 1
	},
	{
		"options": ["if x = 5 {\nprint!(\"{}\", x); }", "if x == 5 {\nprint!(\"{}\", x); }"],
		"correct": 0
	},
	{
		"options": ["fn foo(x: i32) {\nprintln!(\"{}\", x); }", "fn foo(x) {\nprintln!(\"{}\", x); }"],
		"correct": 1
	},
	{
		"options": ["println!(\"Hello, world!)", "println!(\"Hello, world!\")"],
		"correct": 0
	},
	{
		"options": ["vec[1, 2, 3]","vec![1, 2, 3]"],
		"correct": 0
	},
	{
		"options": ["if x == 5 {\nprintln!(\"x is 5\"); }", "if x == 5 {\nprintln!(\"{} is 5\", x); }"],
		"correct": 1
	},
	#17-18
	{
		"options": ["fn get_first<'a>\n(s: &'a str) -> str {\ns.split_whitespace()\n.next().unwrap()}", "fn get_first<'a>\n(s: &'a str) -> &'a str {\ns.split_whitespace()\n.next().unwrap()}"],
		"correct": 0
	},
	{
	"options": ["struct Foo<'a> \n{ bar: &'a str }","struct Foo \n{ bar: &str }"],
	"correct": 0
	},
	#19-21
	{
		"options": [
			"let x = 5; \nlet r = &x;",  
			"let x = 5; \nlet r = &mut x;"  
		],
		"correct": 1
	},
	{
		"options": [
		"let mut x = 10;\n let r: *mut i32 = &mut x;\n *r += 1;",
		"let mut x = 10;\n let r: &mut i32 = &mut x;\n *r += 1;"],
		"correct": 0
	},
	{"options": [
		"let x = Box::new(42);\n println!(\"{}\", *x);",
		"let x = Box::new(42);\n let y = x;\n println!(\"{}\", *x);"
	],
	"correct": 1
	},
	#final boss 
	{
		"options": [
			"let (mut v, c) = \n([1, 0, n], |[l, _, r]:\n[_; 3]| (r - l >> 1) + l);", 
			"let (mut v, c) = \n([1, 0, n], |[l, _, r]:\n[_; 3]| r - l >> 1) + l);"],
		"correct": 0
	}
]

good_responses = [
	"Correct!",
	"Good job!",
	"Nice work!",
	"Keep it up!",
	"Just Like\ni'd do it!",
	"Perfect!",
	"Great!",
]

bad_responses = [
	"Incorrect!",
	"Try again!",
	"Oops!",
	"Keep trying!",
	"Almost!",
	"Did you read\nthe docs?",
	"hey! watch the\nsyntax!",
	"Close, but\nnot quite!",
	"Did you read\bthe book?",
]

def display_questions(dialoge, font):
	options = questions[dialoge]["options"]
	option1_text.text = options[0]
	option2_text.text = options[1]

def clear_options():
	option1_text.text = ""
	option2_text.text = ""
optionfont = bitmap_font.load_font("6x12.bdf")
option1_text = label.Label(optionfont, text="", color=0x000200, line_spacing=0.75)
option1_text.x = 6
option1_text.y = 38

option2_text = label.Label(optionfont, text="", color=0x000200, line_spacing=0.75)
option2_text.x = 6
option2_text.y = 80

def get_response(correct):
	global dialoge
	sleeping = dialoge in range(27, 37)
	if correct:
		if sleeping:
			text_area.text = "zzz"+"z"*(dialoge-27)+"..."
		else: 
			text_area.text = random.choice(good_responses)
	else:
		if sleeping:
			text_area.text = "ZZZ"+"Z"*(dialoge-27)+"!!!"
		else:
			text_area.text = random.choice(bad_responses)

def handle_answer(answer, question):
	global lives
	global life_progress
	if question is None:
		return
	global dialoge
	if questions[question]["correct"] == answer:
		get_response(True)
		life_progress += 1
		if life_progress == 3 & lives < 3:
			lives += 1
			life_progress = 0
			print(lives)
		question = None
	else:
		get_response(False)
		lives -= 1
		question = None
		if lives == 0:
			lose() 
		print(lives) # set the led to the number of lives
	clear_options()
	advance_dialoge()
	next()



font = bitmap_font.load_font("9x18b.bdf")
text_area = label.Label(font, text="", color=0x000000, line_spacing=0.75)
text_area.x = 2
text_area.y = 5

text_boxes = displayio.OnDiskBitmap("text-box.bmp")
text_boxes_sprite = displayio.TileGrid(
	text_boxes,
	pixel_shader=text_boxes.pixel_shader,
	width=1,
	height=1,
	tile_width=128,
	tile_height=128,
	default_tile=0,
	x=0,
	y=128
)

splash.append(bg_sprite)
splash.append(text_area)
splash.append(ferris_sprite)
splash.append(text_boxes_sprite)
splash.append(option1_text)
splash.append(option2_text)

def advance_dialoge():
	global dialoge
	dialoge += 1
	if dialoge >= len(ferris_dialoge):
		win()

def move_ferris(x, y):
	while ferris_sprite.x != x or ferris_sprite.y != y:
		ferris_sprite.x += (x - ferris_sprite.x) // abs(x - ferris_sprite.x) if ferris_sprite.x != x else 0
		ferris_sprite.y += (y - ferris_sprite.y) // abs(y - ferris_sprite.y) if ferris_sprite.y != y else 0
		display.refresh(minimum_frames_per_second=0)
		pygame.time.wait(10)  # Add a small delay to make the movement visible
def win():
	clear_options()
	text_area.text = "You did it!\nCongrats!"
	ferris_sprite[0] = 10
	pygame.time.wait(3000)
	pygame.quit()
	exit()
def lose():
	clear_options()
	text_boxes_sprite.y = -128
	text_area.text = "You lost!\nFerris is sad!"
	ferris_sprite[0] = 9
	pygame.time.wait(3000)
	pygame.quit()
	exit()

def next():
	global question
	if isinstance(ferris_dialoge[dialoge], str):
		question = None
		text_area.text = ferris_dialoge[dialoge]
		advance_dialoge()
	elif isinstance(ferris_dialoge[dialoge], tuple):
		if isinstance(ferris_dialoge[dialoge][0], int):
			move_ferris(ferris_dialoge[dialoge][0], ferris_dialoge[dialoge][1])
			advance_dialoge()
		else:
			question = None
			ferris_sprite[0] = ferris_dialoge[dialoge][1]
			text_area.text = ferris_dialoge[dialoge][0]
			advance_dialoge()
	elif isinstance(ferris_dialoge[dialoge], int):
		question = ferris_dialoge[dialoge]
		display_questions(ferris_dialoge[dialoge], font)
	elif ferris_dialoge[dialoge] == True:
		win()


def intro():
		global lives
		#set screen to black
		# animate cargo run being typed out
		ferris_sprite.x = -64
		text_area.color = 0xFFFFFF
		typed = 0
		# wait for input
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				elif event.type == pygame.KEYDOWN:
						if typed <= len("cargo run"):
							text_area.text += "cargo run "[typed]
							display.refresh(minimum_frames_per_second=1)
							typed += 1
						elif typed > len("cargo_run"):
							if event.key == pygame.K_c:
								lives = 3
								print(lives)
							else:
								lives = 999
							break
			else:
					continue
			break
		text_area.y = 5
		text_area.color = 0x000000
		bg_sprite.y = 0
		ferris_sprite.x = 32
		text_area.text = ferris_dialoge[0]

def main():
	intro() 

	while True:
		
		if question is not None:
			text_boxes_sprite.y = 0
			pass
		else:
			text_boxes_sprite.y = 128
			pass
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z:
					next()
				if event.key == pygame.K_x:
					handle_answer(0, question)
				if event.key == pygame.K_c:
					handle_answer(1, question)

main()