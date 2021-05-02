import pygame, sys
import random
from pygame.locals import *
clock = pygame.time.Clock()

pygame.init()
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))

particles = []
for x in range(1000):
	pixel_size = random.randint(1, 10)
	rect = pygame.Rect(random.randint(0, screen_width-20), random.randint(0, screen_height-20), pixel_size, pixel_size)
	particles.append([rect, 0])

add = -1
while True:
	screen.fill((0, 0, 0))
	
	for particle in particles:
		pygame.draw.rect(screen, (255, 255, 255), particle[0])
		particle_movement = 0
		
		increase_factor = (random.randint(1, 3)/10) * add
		particle[1] += 0.1*add + increase_factor


		if add == 0:
			particle_movement -= particle[1]
		else:
			particle_movement += particle[1]
		particle[0].y += particle_movement


	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				sys.exit()
			if event.key == K_w:
				add = -1
			if event.key == K_s:
				add = 1
	pygame.display.update()
	clock.tick(60)