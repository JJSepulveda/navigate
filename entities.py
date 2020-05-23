import numpy as np
import pandas as pd
import pygame
from pygame.locals import *
import ann

class PVector(object):
	"""
	Crea a un objeto para manipular vectores.

	Parametros
	----------
	x: componente x del vector
	y: componente y del vector

	Retorna
	----------
	Retorna un objeto vector.

	"""
	def __init__(self,x,y):
		self.x = float(x)
		self.y = float(y)
		pass

	def set(self,x,y):
		"""
		Metodo para reasignar las componentes del vector

		Parametros
		----------
		x: componente x del vector
		y: componente y del vector

		Retorna
		----------
		N/A

		"""
		self.x = x
		self.y = y
	
	def mag(self):
		"""
		Metodo para calcular la magnitud del vector

		Parametros
		----------
		usa los valores previamente asignados con set, o cuando se inicializo.

		Retorna
		----------
		float

		"""
		magnitude = (self.x**2 + self.y**2)**0.5

		return magnitude

	def add(self, vector2):
		"""
		Suma los valores de otro vector a las componentes del 
		objeto vector actual.

		Parametros
		----------
		vector2: otro objeto vector

		Retorna
		----------
		N/A

		"""
		self.x += vector2.x
		self.y += vector2.y

	def substract(self, vector2):
		self.x -= vector2.x
		self.y -= vector2.y

	def div(self, d):
		self.x /= d
		self.y /= d

	def multiplication(self, mult):
		self.x *= mult
		self.y *= mult

	def normalize(self):
		magnitude = self.mag()
		self.div(magnitude)

	def limit(self, lim):
		magnitude = self.mag()
		if(magnitude > lim):
			self.normalize()
			self.multiplication(lim)

class Entity(object):
	def __init__(self, x, y, screen_width, scree_height,window):
		default_value = 30
		self.screen_dimensions = {'width': screen_width,'height': scree_height}
		self.velocity_limit = 25
		self.position = PVector(x,y)
		self.velocity = PVector(0,0)
		self.acceleration = PVector(0,0)
		self.width = default_value
		self.height = default_value
		self.color = (0,0,0)
		self.window = window
		pass
	def Update(self):
		self.velocity.add(self.acceleration)
		self.velocity.limit(self.velocity_limit)
		self.position.add(self.velocity)
	def Up_limit(self):
		self.velocity.multiplication(0)
		self.position.y = 0
	def Down_limit(self):
		self.velocity.multiplication(0)
		self.position.y = self.screen_dimensions['height'] - self.height
	def Left_limit(self):
		self.velocity.multiplication(0)
		self.position.x = 0
	def Right_limit(self):
		self.velocity.multiplication(0)
		self.position.x = self.screen_dimensions['width'] - self.width
	def CheckEdge(self):
		max_y = self.screen_dimensions['height']
		max_x = self.screen_dimensions['width']
		condition_up = self.position.y < 0
		condition_down = self.position.y + self.height > max_y
		condition_right = self.position.x + self.width > max_x
		condition_left = self.position.x < 0
		if(condition_up):
			self.Up_limit()
		elif(condition_down):
			self.Down_limit()
		elif(condition_right):
			self.Right_limit()
		elif(condition_left):
			self.Left_limit()
		else: 
			pass
	def Change_color(self, new_color):
		if(type(new_color) is tuple and len(new_color) == 3):
			self.color = new_color
	def Display(self):
		x = np.int32(self.position.x)
		y = np.int32(self.position.y)
		width = np.int32(self.width)
		height = np.int32(self.height)
		pygame.draw.rect(self.window,self.color,(x,y,width,height))

# numero de pasos esta al limite, matar al jugador
# si el jugador esta muerto no debe moverse

class Player(Entity):
	"""
	Crea a un jugador en la posición espesificada.

	Parametros
	----------
	x: posición horizontal de la entidad
	y: posición vertical de la entidad
	screen_width: ancho maximo de la superficie donde se mostrara la entidad
	screen_height: largo maximo de la superficie donde se mostrara la entidad
	window: objeto pygame de la ventana donde se dibujara la entidad

	Retorna
	-----------
	Retorna un objeto entidad
	"""
	def __init__(self, x, y, screen_width, screen_height, window):
		Entity.__init__(self, x, y, screen_width, screen_height, window)

		self.window = window
		self.radius = 10
		self.width = self.radius
		self.height = self.radius
		self.thickness = 1
		self.scale = 1
		velocity_limit = 20
		self.velocity.limit(velocity_limit)
		self.acceleration_value = velocity_limit/2
		self.aceleration_vector = PVector(0,0)
		self.acceleration.limit(velocity_limit)

		inputs = 2
		hidden = 4
		outputs = 4

		self.nn = ann.neuronal_network(inputs,hidden,outputs)

		self.steps = 0
		self.max_steps = 50
		self.fitness = 0
		self.distance_error_amount = 0

		self.Change_color((0,np.random.randint(255),np.random.randint(255)))

	def Fitness(self, target):
		"""
		Calcula la distancia entre el objetivo y este objeto y almacena
		los resultados

		Parametros
		----------
		target: arreglo de 2 dimensiones donde el primer elemento es x y el segundo y

		Retorna
		-----------
		N/A
		"""
		error = PVector(self.position.x - target[0], self.position.y - target[1])
		self.fitness = error.mag()
		self.distance_error_amount += self.fitness
	def Get_fitness(self):
		"""
		Retorna el porcentaje del ultimo desempeño

		Parametros
		----------
		N/A

		Retorna
		-----------
		np.float64
		"""
		return self.distance_error_amount/self.steps

	def Brain(self, pos):

		x = (pos[0] - self.position.x) / self.screen_dimensions['width']
		y = (pos[1] - self.position.y) / self.screen_dimensions['height']		

		p = self.nn.predict([x, y])

		index_of_max = np.argmax(p)

		if(index_of_max == 0):
			self.Up_key_pressed()
		elif(index_of_max == 1):
			self.Down_key_pressed()
		elif(index_of_max == 2):
			self.Right_key_pressed()
		elif(index_of_max == 3):
			self.Left_key_pressed()

		self.Fitness((pos[0], pos[1]))

		#para darle un limite de pasos y pasar a la siguiente generacion
		#cada vez que se llama a esta funcion significa que se de un paso
		#asi que se suma un paso al numero maximo de pasos.
		#self.steps += 1

		pass
	def Change_size(self, new_size):
		"""
		Cambia el tamaño del objeto que se dibuja en la superficie de trabajo.

		Parametros
		----------
		new_size: tamaño nuevo deseado

		Retorna
		-----------
		N/A
		"""
		self.radius = new_size
	def Scale(self, scale):
		"""
		Cambia la escala del objeto dibujado en la superficie de trabajo.

		Parametros
		----------
		scale: valor de la escala.

		Retorna
		-----------
		N/A
		"""
		self.scale = scale
	def Up_key_pressed(self):
		self.aceleration_vector.set(0,-self.acceleration_value)
		self.acceleration.add(self.aceleration_vector)
		self.steps += 1
		pass
	def Down_key_pressed(self):
		self.aceleration_vector.set(0,self.acceleration_value)
		self.acceleration.add(self.aceleration_vector)
		self.steps += 1
		pass
	def Right_key_pressed(self):
		self.aceleration_vector.set(self.acceleration_value,0)
		self.acceleration.add(self.aceleration_vector)
		self.steps += 1
		pass
	def Left_key_pressed(self):
		self.aceleration_vector.set(-self.acceleration_value,0)
		self.acceleration.add(self.aceleration_vector)
		self.steps += 1
		pass
	def Move(self):
		self.CheckEdge()
		self.Update()
		self.acceleration.set(0,0)
		self.velocity.set(0,0)
	def Get_cordinates(self):
		x = self.position.x
		y = self.position.y
		return [x, y]
	def Get_values(self):
		x = self.position.x
		y = self.position.y
		w = self.width
		h = self.height
		return [x, y, w, h]
	def Reset(self):
		self.position.set(self.screen_dimensions['width']/2,self.screen_dimensions['height']/2)
		self.acceleration.set(0,0)
		self.velocity.set(0,0)
		self.steps = 0
		self.fitness = 0
		self.distance_error_amount = 0
	def Display(self):
		surface = self.window
		color = self.color
		x = np.int32(self.position.x)
		y = np.int32(self.position.y)
		radius = self.radius * self.scale
		#width = self.thickness
		pygame.draw.circle(surface, color, (x,y), radius)
	def Live_success(self):
		success = False
		if(self.steps >= self.max_steps):
			success = True
		return success
	def Colision(self, target_values):
		colision = False

		target_x = target_values[0]
		target_y = target_values[1]
		target_w = target_values[2]
		target_h = target_values[3]

		my_right_limit = self.position.x + self.radius
		my_left_limit = self.position.x - self.radius
		my_upper_limit = self.position.y - self.radius
		my_bottom_limit = self.position.y + self.radius
		your_left_limit = target_x - target_w
		your_right_limit = target_x + target_w
		your_upper_limit = target_y - target_h
		your_bottom_limit = target_y + target_h

		colision_y_up_to_bot = my_bottom_limit > your_upper_limit and \
								my_bottom_limit < your_bottom_limit

		colision_y_bot_to_up = my_upper_limit < your_bottom_limit and \
								my_upper_limit > your_upper_limit 

		colision_x_left_to_right = my_right_limit > your_left_limit and \
									my_right_limit < your_right_limit 

		colision_x_right_to_left = my_left_limit < your_right_limit and \
									my_left_limit > your_left_limit 

		colision_condition = (colision_x_left_to_right or colision_x_right_to_left) and \
								(colision_y_up_to_bot or colision_y_bot_to_up)

		if(colision_condition):
			colision = True

		return colision
	def Get_brain(self):
		return self.nn.get_weights_and_bias()
	def Set_new_brain(self,buff):
		self.nn.set_weights_and_bias(buff)