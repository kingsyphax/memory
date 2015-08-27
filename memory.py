import pygame
from pygame.locals import *
from sys import exit
from random import *

class MemoryCard(pygame.surface.Surface):
	'''A memory card'''
	def __init__(self, image, altimage, x, y):
		'''Set position and initial vector of the ball
		x and y are center of the ball'''
		pygame.surface.Surface.__init__(self, (80, 120)) # call superclass constructor
		self.image = image # set sprite's image
		self.alternateimage = altimage
		self.left = x - image.get_width()/2 # compute upper-left corner of ball
		self.top = y - image.get_height()/2
		self.rect = pygame.Rect(self.left, self.top, # build the rectangle
								80,
								120)
		self.visible = True

	def switch(self):
		'''Switches main and alternate image'''
		temp = self.image
		self.image = self.alternateimage
		self.alternateimage = temp

	def draw(self, screen):
		'''Draws ball to screen object'''
		screen.blit(self.image,self.rect)

# initialize pygame and screen window
pygame.init()
screen = pygame.display.set_mode((720, 450))
pygame.display.set_caption('Memory') # title of window

aragorn = pygame.image.load('/Users/nicholasward/Desktop/Programming/Python/Memory/aragorn.png').convert() # get image file
gollum = pygame.image.load('/Users/nicholasward/Desktop/Programming/Python/Memory/gollum.png').convert()
legolas = pygame.image.load('/Users/nicholasward/Desktop/Programming/Python/Memory/legolas.png').convert()
frodo = pygame.image.load('/Users/nicholasward/Desktop/Programming/Python/Memory/frodo.png').convert()
blank = pygame.image.load('/Users/nicholasward/Desktop/Programming/Python/Memory/blank.png').convert()

# put card in center of screen, moving at 100 pixels/second
card1 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 - 100,
						  y = screen.get_height()/2 - 100)
card2 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 + 100,
						  y = screen.get_height()/2 - 100)
card3 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 - 100,
						  y = screen.get_height()/2 + 100)
card4 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 + 100,
						  y = screen.get_height()/2 + 100)
card5 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 - 300,
						  y = screen.get_height()/2 - 100)
card6 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 + 300,
						  y = screen.get_height()/2 - 100)
card7 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 - 300,
						  y = screen.get_height()/2 + 100)
card8 = MemoryCard(image = blank, altimage = blank,
						  x = screen.get_width()/2 + 300,
						  y = screen.get_height()/2 + 100)

size = 8
cards = (card1, card2, card3, card4, card5, card6, card7, card8)

#ARAGORN
aragornFirst = randint(0, size-1)
cards[aragornFirst].alternateimage = aragorn

aragornSecond = randint(0, size-1)
while cards[aragornSecond].alternateimage != blank:
	aragornSecond = randint(0, size-1)
cards[aragornSecond].alternateimage = aragorn

#LEGOLAS AND FRODO
for i in range(2): #repeat twice
	legolasCurrent = randint(0, size-1)
	while cards[legolasCurrent].alternateimage != blank:
		legolasCurrent = randint(0, size-1)
	cards[legolasCurrent].alternateimage = legolas
	frodoCurrent = randint(0, size-1)
	while cards[frodoCurrent].alternateimage != blank:
		frodoCurrent = randint(0, size-1)
	cards[frodoCurrent].alternateimage = frodo

#GOLLUM
for card in cards:
	if card.alternateimage == blank: #not any of the others
		card.alternateimage = gollum

clock = pygame.time.Clock() # for timing 

def inside(mouseX, mouseY, card):
	if mouseX < card.left or mouseX > card.left + 80:
		return False
	if mouseY < card.top or mouseY > card.top + 120:
		return False
	return True
	
def isShown(card): # boolean: is the card face-up?
	return not (card.image == blank)

def areShown(cards): # int: how many cards are face-up?
	count = 0
	for card in cards:
		if isShown(card): count += 1
	return count
	
def cardsAreSame(cards): # the two cards showing have the same image
	theImage = 0
	for card in cards:
		if isShown(card):
			if theImage == 0:
				theImage = card.image
			else:
				return card.image == theImage

def deleteCards(cards): # delete all showing cards
	for card in cards:
		if isShown(card):
			card.visible = False
			card.switch()

turnsCount = 0

clock = pygame.time.Clock()
while True: # main loop
	cardsAreVisible = False
	for card in cards:
		if card.visible == True: cardsAreVisible = True
	if not cardsAreVisible:
		pygame.time.delay(2000)
		exit()
		
	if areShown(cards) == 2: #turn over
		turnsCount += 1
		pygame.time.delay(500)
		if cardsAreSame(cards):
			deleteCards(cards)
		else:
			for card in cards:
				if isShown(card):
					card.switch()
	for event in pygame.event.get(): # get all events
		if event.type == QUIT: # check for clicking close box
			exit()
		if event.type == MOUSEBUTTONDOWN:
			mouseX = event.pos[0]
			mouseY = event.pos[1]
			for card in cards:
				if inside(mouseX, mouseY, card) and not isShown(card):
					card.switch()

	timePassed = clock.tick(30)

	screen.fill(pygame.color.Color('red'))
	font = pygame.font.SysFont("Helvetica",18)
	ren = font.render("Turns: %d"%turnsCount,1,pygame.color.Color('black'))
	screen.blit(ren, (630,20))
	for card in cards:
		if card.visible: card.draw(screen)
	pygame.display.update() # update everything