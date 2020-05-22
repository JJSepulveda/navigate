import numpy as np
import pandas as pd
import time
import pygame
from pygame.locals import *
import entities
import sys

WIDTH = 500
HEIGHT = 500
WIDTH_PANEL = 300

pygame.init()
window = pygame.display.set_mode((WIDTH+WIDTH_PANEL,HEIGHT))
pygame.display.set_caption("Navigate")

BACKGROUND_COLOR = (255,255,255)

def background():
	window.fill((BACKGROUND_COLOR))
	points = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
	pygame.draw.polygon(window, (0, 0, 0), points, 3)

def text(txt,x,y, textColor = (0, 0, 0)):
	font = pygame.font.Font("C:/Windows/Fonts/COOPBL.TTF",14)
	text = font.render(txt, True, textColor)
	window.blit(text, (x, y))

# 1. crear poblacion
# 2. calcular aptitud
# 3. torneo
# 4. cruza de los mas aptos
# 5. nueva generacion
# 6. vuelve al paso 2 hasta acabar el numero de generaciones

def main():
	
	player = entities.Player(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, window)

	target = entities.Player(np.random.randint(WIDTH), np.random.randint(HEIGHT), WIDTH, HEIGHT, window)

	target.Change_color((255,0,0))

	# tiempo de retraso en milisegundos en la primera repetición
	delay = 101
	# intervalo de tiempo en milisegundos entre repeticiones
	interval = 100
	# habilita la repetición de teclas
	pygame.key.set_repeat(delay, interval)

	while(True):
		background()

		text("Generación: ", WIDTH + 10, 50)
		text("Población: ", WIDTH + 10, 70)
		text("Error: ", WIDTH + 10, 90)
		
		#player.Brain(target.Get_cordinates())

		success = player.Live_success()

		finish = player.Colision(target.Get_values())

		if(success or finish):
			print("success")
			print(player.Get_fitness())
			target.Display()
		else:
			player.Move()
			player.Display()
			target.Move()
			target.Display()

		
		for event in pygame.event.get():
			if (event.type == QUIT):
				pygame.quit()
				sys.exit()
			if(event.type == KEYDOWN):
				if(event.key == pygame.K_w):
					player.Up_key_pressed()
					player.Fitness(target.Get_cordinates())
				if(event.key == pygame.K_s):
					player.Down_key_pressed()
					player.Fitness(target.Get_cordinates())
				if(event.key == pygame.K_d):
					player.Right_key_pressed()
					player.Fitness(target.Get_cordinates())
				if(event.key == pygame.K_a):
					player.Left_key_pressed()
					player.Fitness(target.Get_cordinates())

		pygame.display.update()
		time.sleep(0.025)

if(__name__ == '__main__'):
	main()
