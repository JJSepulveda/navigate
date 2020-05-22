####################################
## Algoritmo genetico
####################################
import numpy as np


class AG(object):
	def __init__(self,population):
		#el numer de poblacion tiene que ser par
		self.population = np.uint32(population)
		#self.participants = np.uint32(self.population * 0.05)
		self.participants = 5
		self.winners = []
		self.actual_generation = 0
		self.mutation_probability = 0.1
	def crossover(self, dad, mother):
		variable_type = 64 #float 64
		parent1 = dad['cromosomas'].reshape(-1)
		parent2 = mother['cromosomas'].reshape(-1)

		#lo multiplicamos por el tipo de variable ya que la cruza se 
		#hara a nivel de bits.
		leng = (len(parent1) * variable_type) - 1
		screw_point = np.random.randint(leng)
		#lo dividimos entre el numer ode bits del tipo de variable
		#y nos da la posición en el arreglo
		index_of_screw = screw_point/variable_type
		#no se me ocurrio otra cosas mas queagregar este if para 
		#que cuando la division diera 0 no se use el operador modulo
		#porque no funciona porque es una division entre 0
		if(index_of_screw<1):
			bit_index = index_of_screw * variable_type
			pass
		else:
			bit_index = (index_of_screw % np.floor(index_of_screw)) * variable_type
		#Convertimos la variable bit_index ahora porque en unas cuantas lineas mas se usara
		#este indice como corrimiento para una mascara y el operador de corrimiento
		#no acepta variables del tipo float para realziar su funcion.
		bit_index = np.uint8(bit_index)
		index_of_screw = np.floor(index_of_screw)
		index_of_screw = np.uint64(index_of_screw)

		#partimos el elemento
		mask = np.uint64(0)
		mask = ~mask << bit_index
		#lo multiplicamos por mil debido a que lo estamos transformando
		#a un tipo de datos que no maneja decimales y si no se multiplica
		#se pierden los decimals. Posteriormente lo reconvertimos y se divide
		#entre 1000.
		sign_parent1 = False
		if(parent1[index_of_screw] < 0):
			parent1[index_of_screw] *= -1
			sign_parent1 = True
		target_value = np.uint64(parent1[index_of_screw] * 1000)
		first_cut_parent1 = (target_value & mask) 
		second_cut_parent1 = (target_value & ~mask)

		#guardamos el signo porque las operaciones bitwise solo son compatibles
		#con variables sin signo.
		sign_parent2 = False
		if(parent2[index_of_screw] < 0):
			parent2[index_of_screw] *= -1
			sign_parent2 = True
		target_value = np.uint64(parent2[index_of_screw] * 1000)
		first_cut_parent2 = (target_value & mask)
		second_cut_parent2 = (target_value & ~mask)

		child_single_value1 = np.float64( (second_cut_parent1 | first_cut_parent2) /1000)
		child_single_value2 = np.float64( (first_cut_parent1 | second_cut_parent2) /1000)

		#recuperamos el signo.
		#estoy pensando en poner que el signo se recupera aleatoriamente.
		if(sign_parent1):
			child_single_value1 *= -1

		if(sign_parent2):
			child_single_value2 *= -1

		parent2[index_of_screw] = child_single_value1
		child1 = parent1[0:index_of_screw]
		child1 = np.append(child1, parent2[index_of_screw:])

		parent1[index_of_screw] = child_single_value2
		child2 = parent2[0:index_of_screw]
		child2 = np.append(child2, parent1[index_of_screw:])

		return np.array([child1.reshape(dad['cromosomas'].shape), child2.reshape(dad['cromosomas'].shape)])
	def crossover_32(self, dad, mother):
		"""
		Cruza dos arreglos y crea dos hijos

		Parametros
		----------
		dad: arraglo 
		mother: arreglo

		Retorna
		-----------
		np.float64 (2, dad.shape)
		"""
		variable_type = 32 #float 32
		offset = 100000
		parent1 = dad['cromosomas'].reshape(-1)
		parent2 = mother['cromosomas'].reshape(-1)

		#lo multiplicamos por el tipo de variable ya que la cruza se 
		#hara a nivel de bits.
		leng = (len(parent1) * variable_type) - 1
		screw_point = np.random.randint(leng)
		#lo dividimos entre el numer ode bits del tipo de variable
		#y nos da la posición en el arreglo
		index_of_screw = screw_point/variable_type
		#no se me ocurrio otra cosas mas queagregar este if para 
		#que cuando la division diera 0 no se use el operador modulo
		#porque no funciona porque es una division entre 0
		if(index_of_screw<1):
			bit_index = index_of_screw * variable_type
			pass
		else:
			bit_index = (index_of_screw % np.floor(index_of_screw)) * variable_type
		#Convertimos la variable bit_index ahora porque en unas cuantas lineas mas se usara
		#este indice como corrimiento para una mascara y el operador de corrimiento
		#no acepta variables del tipo float para realziar su funcion.
		bit_index = np.uint8(bit_index)
		index_of_screw = np.floor(index_of_screw)
		index_of_screw = np.uint32(index_of_screw)

		#partimos el elemento
		mask = np.uint32(0)
		mask = ~mask << bit_index
		#lo multiplicamos por mil debido a que lo estamos transformando
		#a un tipo de datos que no maneja decimales y si no se multiplica
		#se pierden los decimals. Posteriormente lo reconvertimos y se divide
		#entre 1000.
		sign_parent1 = False
		if(parent1[index_of_screw] < 0):
			parent1[index_of_screw] *= -1
			sign_parent1 = True
		target_value = np.uint32(parent1[index_of_screw] * offset)
		first_cut_parent1 = (target_value & mask) 
		second_cut_parent1 = (target_value & ~mask)

		#guardamos el signo porque las operaciones bitwise solo son compatibles
		#con variables sin signo.
		sign_parent2 = False
		if(parent2[index_of_screw] < 0):
			parent2[index_of_screw] *= -1
			sign_parent2 = True
		target_value = np.uint32(parent2[index_of_screw] * offset)
		first_cut_parent2 = (target_value & mask)
		second_cut_parent2 = (target_value & ~mask)

		child_single_value1 = np.float64( (second_cut_parent1 | first_cut_parent2) /offset)
		child_single_value2 = np.float64( (first_cut_parent1 | second_cut_parent2) /offset)

		#recuperamos el signo.
		#estoy pensando en poner que el signo se recupera aleatoriamente.
		if(sign_parent1):
			child_single_value1 *= -1

		if(sign_parent2):
			child_single_value2 *= -1

		parent2[index_of_screw] = child_single_value1
		child1 = parent1[0:index_of_screw]
		child1 = np.append(child1, parent2[index_of_screw:])

		parent1[index_of_screw] = child_single_value2
		child2 = parent2[0:index_of_screw]
		child2 = np.append(child2, parent1[index_of_screw:])

		return np.array([child1.reshape(dad['cromosomas'].shape), child2.reshape(dad['cromosomas'].shape)])
	def tournament (self):
		#arreglo de un numero entero entre 0 y el tamaño total de los participantes,
		#del tamaño de la cantidad de participantes.

		winners = []

		#para que este algoritmo funciones se el buffer tiene que estar ordenado de mayor a menor
		#con respecto al fitness
		for _ in range(self.population):
			participants_id = np.random.randint(0, self.population - 1, (self.participants))
			winners.append(np.max(participants_id))

		winners = winners
		self.winners = winners
	def first_generation(self):
		return np.random.randn(self.population,4,2)
	def get_generation(self):
		return self.actual_generation
	def mutation(self,target):
		dice = np.random.randint(1,100)
		probability = self.mutation_probability * 100
		#si hay mutación cambiamos el signo.
		if(dice <= probability):
			target += np.random.normal(size=target.shape[0],loc = 0, scale=0.5)

	def new_generation(self,buff):

		self.tournament()
		childs = []
		#para que range funciones tiene que ser un entero
		amount = self.population//2

		for _ in range(amount):
			dad = buff[self.winners[0]]
			mother = buff[self.winners[1]]
			c1, c2 = self.crossover_32(dad,mother)
			self.mutation(c1)
			self.mutation(c2)
			childs.append(c1)
			childs.append(c2)
			self.winners.pop(0)
			self.winners.pop(0)

		self.actual_generation += 1
		#print("childs shape: {}".format((np.asarray(childs)).shape))
		#print("Generación acual: {}".format(self.actual_generation))

		return childs

def fit(array):
	x = 1
	y = 1
	target = 13
	fit = np.absolute(target - (array[0]*x + array[1]*y + array[2]))
	return fit

if(__name__ == '__main__'):
	POPULATION = 50
	shape = 3
	dt = np.dtype([('cromosomas', np.float64, (shape,)), ('fitness', np.float64)])
	array = np.array([],dtype = dt)
	array_t = np.array([],dtype = dt)
	
	for i in range(POPULATION):
		a = np.random.randint((255,255,255))
		fitness = fit(a)
		values = np.array((a,fitness), dtype = dt)
		array = np.append(array,values)
	print("-------------------------")
	print(array[0]['cromosomas'])
	print("-------------------------")

	ag = AG(POPULATION)

	generation = 100

	while(generation):
		array = np.sort(array, order='fitness')
		print("-------------------------")
		print("fitness: {}".format(array[0]['fitness']))
		print("fitness: {}".format(array[1]['fitness']))
		print("fitness: {}".format(array[2]['fitness']))
		print("-------------------------")
		childs = ag.new_generation(array)
		for i in childs:
			fitness = fit(i)
			values = np.array((i,fitness), dtype = dt)
			array_t = np.append(array_t,values)
		array = np.copy(array_t)
		for _ in array_t:
			array_t = np.delete(array_t,0)
		generation -= 1

	print("cromosoma: {}, fit: {}".format(array[0]['cromosomas'],array[0]['fitness']))
	print("cromosoma: {}, fit: {}".format(array[1]['cromosomas'],array[1]['fitness']))


	#dad = np.array([[-1.0,1.0,1.0,1.0],[-2.0,2.0,2.0,2.0]])
	#dad = np.random.randn(4,2)
	#mot = np.array([[-3.0,3.0,3.0,3.0],[-4.0,4.0,4.0,4.0]])
	#dad, mot = ag.crossover_32(dad,mot)
	#ag.mutation(dad)
	#print(dad)
	#print(mot)
	#fg = ag.first_generation()
	#ag.new_generation(fg)