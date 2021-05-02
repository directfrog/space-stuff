import pygame
import sys, os, random
from pygame.locals import *
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

class Game(object):
	def __init__(self):

		##### Screen Values #####
		self.screen_width = 600
		self.screen_height = 600
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))#
		
		##### Initiates the particle system #####
		self.particles = []
		for x in range(1000):
			pixel_size = random.randint(1, 10)
			y_pos = random.randint(-25000, 0)
			x_pos = random.randint(5, self.screen_width-10)
			rect = pygame.Rect(x_pos, y_pos, pixel_size, pixel_size)
			self.particles.append([rect, 0])
		self.direction = 1

		##### Player values #####	
		self.player_rect = pygame.Rect(100, 100, 25, 80)
		self.moving_left = False
		self.moving_right = False
		self.jump = False
		self.x_vel = 2
		self.vertical_momentum = 0
		self.idle = pygame.image.load('idle.png').convert()
		self.idle.set_colorkey((0, 0, 0))
		self.idle = pygame.transform.scale(self.idle, (25, 80))
		self.rotat = self.idle

		self.jumping = pygame.image.load('jump.png').convert()
		self.jumping.set_colorkey((0, 0, 0))
		self.jumping = pygame.transform.scale(self.jumping, (25, 80))
		self.rocks = []
		self.rock_img = pygame.image.load('rock.png')
		self.rock_img = pygame.transform.scale(self.rock_img, (32, 32))
		self.returning = []


	def return_screen(self):
		return self.screen
	
	def update_fill(self):
		self.screen.fill((0, 0, 0))

	def handle_movement(self):
		self.player_movement = [0, 0]

		##### movement #####
		if self.moving_left == True:
			self.player_movement[0] = -self.x_vel
			self.rotat = pygame.transform.flip(self.idle, True, False)
		if self.moving_right == True:
			self.player_movement[0] = self.x_vel
			self.rotat = self.idle
		if self.jump:
			self.vertical_momentum = -5

		##### simulating gravity #####
		if self.player_rect.y < 400:
			self.vertical_momentum += 0.2
		else:
			if not self.jump:
				self.vertical_momentum = 0
		self.player_movement[1] += self.vertical_momentum

			
	
	def handle_input(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()
				if event.key == K_a:
					self.moving_left = True
				if event.key == K_d:
					self.moving_right = True
				if event.key == K_SPACE:
					self.jump = True
			if event.type == KEYUP:
				if event.key == K_a:
					self.moving_left = False
				if event.key == K_d:
					self.moving_right = False
				if event.key == K_SPACE:
					self.jump = False

	def handle_collisions(self):
		hit_list = [rock for rock in self.rocks if self.player_rect.colliderect(rock)]
		for rock in hit_list:
			if self.player_rect.bottom > rock.top:
				self.vertical_momentum = 0


	def update_screen(self):
		##### player position updating #####
		self.screen.blit(self.rotat, (self.player_rect.x, self.player_rect.y))
		self.player_rect.x += self.player_movement[0]
		self.player_rect.y += self.player_movement[1]


		##### Particles updating #####
		for particle in self.particles:
			if particle[0].y < self.screen_height:
				pygame.draw.rect(self.screen, (255, 255, 255), particle[0])
				particle_movement = 0
				
				increase_factor = (random.randint(1, 3)/10) * self.direction
				particle[1] += 0.1*self.direction #+ increase_factor

				if particle[1] > 3:
					particle[1] = 3

				if self.direction == 0:
					particle_movement -= particle[1]
				else:
					particle_movement += particle[1]
				particle[0].y += particle_movement
			else:
				y_pos = random.randint(-50000, 0)
				x_pos = random.randint(5, self.screen_width-10)
				particle[0].y = y_pos
				particle[0].x = x_pos

		tile_range = [self.player_rect.x-self.screen_width, self.player_rect.x+self.screen_width]
	
		##### Draws a layer of rock #####
		for x_val in range(self.player_rect.x-self.screen_width, self.player_rect.x+self.screen_width):
			if x_val % 32 == 0:
				tile_rect = pygame.Rect(x_val, 400, 32, 32) 
				if tile_rect not in self.rocks:
					self.rocks.append(tile_rect)
	
		for rock in self.rocks:
			if rock.x < tile_range[0] or rock.x > tile_range[1]:
				self.rocks.pop(self.rocks.index(rock))

		for rock in self.rocks:
			screen.blit(self.rock_img, (rock.x, rock.y))
	
		print(len(self.rocks))

game = Game()
screen = game.return_screen()


##### Plays the music #####
pygame.mixer.init()
pygame.mixer.music.load("soundtrack.wav")
#pygame.mixer.music.play(-1)

while True:
	game.update_fill()

	game.handle_movement()
	game.handle_input()

	game.handle_collisions()
	game.update_screen()
		
	pygame.display.update()
	clock.tick(120)
