import numpy as np
import pandas as pd
import time
import pygame
from pygame.locals import *
import entities
import sys
import AG

WIDTH = 500
HEIGHT = 500
WIDTH_PANEL = 300
MAX_POPULATION = 200
GAME_MODE = 0
MACHINE_LEARNING_MODE = 1
HUMAN_MODE = 2

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

def make_population():
	population_array = np.array([])

	for _ in range(MAX_POPULATION):
		element = entities.Player(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, window)
		population_array = np.append(population_array, element)

	return population_array

def generation_duty(generation_array, target):
	finish = False
	colision = False
	amount_of_succesfully_players = 0

	target_values = target.Get_values()

	for i in generation_array:
		colision = i.Colision(target_values)
		live_success = i.Live_success()
		if(colision or live_success):
			amount_of_succesfully_players += 1
		else:
			i.Brain([target_values[0], target_values[1]])
			i.Move()
			i.Display()

	if(amount_of_succesfully_players == len(generation_array)):
		finish = True

	return finish

def generation_reset(generation_array):
	for i in generation_array:
		i.Reset()

def generation_sort(generation_array):
	dt = np.dtype([('cromosomas', np.float64, (generation_array[0].Get_brain().shape[0],)), ('fit', np.float64)])
	sorted_array = np.array([], dtype=dt)
	for i in generation_array:
		values = np.array((i.Get_brain(), i.Get_fitness()), dtype = dt)
		sorted_array = np.append(sorted_array, values)

	sorted_array = np.sort(sorted_array, order='fit')
	return sorted_array

def generation_rewrite_brain(generation_array, new_generation):
	for i,p in enumerate(generation_array):
		p.Set_new_brain(new_generation[i])


# 1. crear poblacion
# 2. calcular aptitud
#	2.1 una vez que termine el procesamiento, calcualr la actitud
# 3. ordenar
# 3. torneo
# 4. cruza de los mas aptos
# 5. nueva generacion
# 6. vuelve al paso 2 hasta acabar el numero de generaciones

def main():
	
	player = entities.Player(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, window)
	target = entities.Player(15, HEIGHT-15, WIDTH, HEIGHT, window)
	target.Change_color((255,0,0))
	# tiempo de retraso en milisegundos en la primera repetición
	delay = 101
	# intervalo de tiempo en milisegundos entre repeticiones
	interval = 100
	# habilita la repetición de teclas
	pygame.key.set_repeat(delay, interval)

	players_array = make_population()
	GAME_MODE = MACHINE_LEARNING_MODE

	ag = AG.AG(MAX_POPULATION)

	while(True):

		background()

		text("Generación: ", WIDTH + 10, 50)
		text("Población: ", WIDTH + 10, 70)
		text("Error: ", WIDTH + 10, 90)

		target.Display()
		
		#player.Brain(target.Get_cordinates())
		if(GAME_MODE == MACHINE_LEARNING_MODE):
			
			generation_finish_flag = generation_duty(players_array, target)

			if(generation_finish_flag):
				#ordenar el arreglo
				sorted_array = generation_sort(players_array)
				new_generation_array = ag.new_generation(sorted_array)
				print("--------------------------------")
				print(sorted_array[0]['fit'])
				print(sorted_array[1]['fit'])
				print(sorted_array[2]['fit'])
				print(sorted_array[3]['fit'])
				#print(new_generation_array)
				#print(new_generation_array)
				print("--------------------------------")
				generation_rewrite_brain(players_array, new_generation_array)
				generation_reset(players_array)
				generation_finish_flag = False
				pass


		elif(GAME_MODE == HUMAN_MODE):
			
			success = player.Live_success()

			finish = player.Colision(target.Get_values())

			if(success or finish):
				print(player.Get_fitness())
				player.Reset()
			else:
				player.Brain(target.Get_values())
				player.Move()
				player.Display()
		
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
