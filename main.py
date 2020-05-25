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
FPS = 60


pygame.init()
window = pygame.display.set_mode((WIDTH+WIDTH_PANEL,HEIGHT))
pygame.display.set_caption("Navigate")
fpsClock = pygame.time.Clock()

BACKGROUND_COLOR = (255,255,255)
g_file_name = "backup.csv"

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

def neuronal_network_backup(buff):
	file_name = g_file_name
	values = []
	fitness = []
	dataframe = {'cromosomas': [], 'fitness': []}
	#convierto el arreglo cromosomas porque cuando se guarda en csv
	#se pierde el tipo de datos array, asi que es mejor guardarla
	#como una string y cuando se recuperen los datos se reconvierten a array.
	for i in buff:
		string = np.array2string(i['cromosomas'], precision=6, separator=' ', suppress_small=True)
		values.append(string[1:-1])
		fitness.append(i['fit'])

	dataframe['cromosomas'] = values
	dataframe['fitness'] = fitness
	
	dataframe = pd.DataFrame(dataframe)
	print(dataframe)
	dataframe.to_csv(file_name)

def convert_string_to_array(pixels):
	if type(pixels) == str:
		pixels = np.array([np.float64(i) for i in pixels.split()])	
	return pixels


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

	actual_generation = 0

	players_array = make_population()
	GAME_MODE = HUMAN_MODE

	ag = AG.AG(MAX_POPULATION)

	#se recupeara la red nueronal anteriormente guardada y se inserta
	#en un jugador individual para corroborar su rendimiento.
	backup_nn = pd.read_csv(g_file_name)
	best_nn = convert_string_to_array(backup_nn['cromosomas'][0])
	print(best_nn)
	player.Set_new_brain(best_nn)

	while(True):

		background()

		actual_generation = ag.get_generation()

		text("Generación: {}".format(actual_generation), WIDTH + 10, 50)
		text("Población: {}".format(MAX_POPULATION), WIDTH + 10, 70)
		text("Error: ", WIDTH + 10, 90)
		target.Display()

		if(GAME_MODE == MACHINE_LEARNING_MODE):
			#actualizar las posiciones y la visualizacion de los jugadores.
			generation_finish_flag = generation_duty(players_array, target)

			if(generation_finish_flag):
				#ordenar el arreglo
				sorted_array = generation_sort(players_array)
				#crear la nueva generacion
				new_generation_array = ag.new_generation(sorted_array)
				#reescribir los datos en los jugadores
				generation_rewrite_brain(players_array, new_generation_array)
				#resetar las posiciones
				generation_reset(players_array)
				generation_finish_flag = False
				#cambiar el lugar del objetivo
				target.position.set(np.random.randint(WIDTH), np.random.randint(HEIGHT))
				pass

		elif(GAME_MODE == HUMAN_MODE):
			
			success = player.Live_success()

			finish = player.Colision(target.Get_values())

			if(success or finish):
				print(player.Get_fitness())
				player.Reset()
				#Cambiamos la posición del objetivo para asegurarnos que la red aprendio para 
				#cualquier posición y no esta sesgada.
				target.position.set(np.random.randint(WIDTH), np.random.randint(HEIGHT))
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
				if(event.key == pygame.K_g):
					neuronal_network_backup(sorted_array[0:10])

		pygame.display.update()
		fpsClock.tick(FPS)
		#time.sleep(0.025)

if(__name__ == '__main__'):
	main()