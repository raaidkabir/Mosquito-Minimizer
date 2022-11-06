import random
import mesa.time
import numpy as np
from mesa import Model, Agent
from mesa.space import ContinuousSpace
from src.helper import *

class Mosquito_model(Model):
	def __init__(self, Mosquito_count, Dragonfly_count, width, height, WINDOW):
		self.count = 0
		self.schedule = mesa.time.RandomActivation(self)
		self.space = ContinuousSpace(width+1, height+1, torus=False)
		self.step_num = 0
		self.prev_id = 0
		self.canvas = WINDOW
		self.has_food_ticks = {}
		self.Mosquito_count = 0
		self.Dragonfly_count = 0
	
		for x, y in cartesian([np.arange(width), np.arange(height)]):
			new_cell = Cell(self.new_id(), self)
			self.space.place_agent(new_cell, (x, y))
			new_cell.canvas = WINDOW
			new_cell.draw()

		for _ in range(Mosquito_count):
			x = y = random.randrange(self.space.width)
			self.give_birth(x, y, age= np.random.randint(1, 5), kind='Mosquito')
		for _ in range(Dragonfly_count):
			x = y = random.randrange(self.space.width)
			self.give_birth(x, y, age= np.random.randint(1, 4), kind='Dragonfly')

	def kill(self, selected):
		if selected.kind == 'Mosquito':
			self.Mosquito_count -= 1
		else:
			self.Dragonfly_count -= 1
		x_1, y_1 = get_cell_bounds(selected.pos)[:2]
		self.canvas.delete(selected.image)
		self.count -= 1
		self.space.remove_agent(selected)
		self.schedule.remove(selected)
		self.canvas.create_text(x_1, y_1, text="†", font=12, justify='center')

	def new_id(self):
		id = self.prev_id + 1
		self.prev_id = id
		return id

	def give_birth(self, x, y, age=0, kind='Mosquito'):
		if kind == 'Mosquito':
			a = Mosquito(self.new_id(), self, age=age)
			self.Mosquito_count += 1
		else:
			a = Dragonfly(self.new_id(), self, age=age)
			self.Dragonfly_count += 1
		self.schedule.add(a)
		self.space.place_agent(a, (x, y))
		self.count += 1
		a.canvas = self.canvas
		a.draw()

	def step(self):
		self.step_num += 1

		if self.step_num in self.has_food_ticks:
			for grass in self.has_food_ticks[self.step_num]:
				grass.replenish()
			del self.has_food_ticks[self.step_num]

		self.schedule.step()


class Cell(Agent):
	def __init__(self, id, model):
		super().__init__(id, model)
		self.id = id
		self.has_food = 0
		if np.random.random() < WATER_AREA:
			self.kind = 'Water'
		else:
			self.kind = 'Grass'
			if np.random.random() < FEEDING_AREA:
				self.has_food = 1.0

	def replenish(self):
		self.has_food = 1
		self.update()

	def paint_cell(self):
		if self.has_food >= 1:
			return "#387F0A"
		elif self.kind == 'Water':
			return "#71BCFA"
		return "#42C744"

	def update(self):
		self.canvas.itemconfig(self.image, fill=self.paint_cell())

	def consume(self):
		self.has_food = 0
		self.update()
		step = int(self.model.step_num + FOOD_REPLENISH // AGE_DELTA)
		g = self.model.has_food_ticks.get(step, [])
		g.append(self)
		self.model.has_food_ticks[step] = g

	def draw(self):
		self.image = self.canvas.create_rectangle(*get_cell_bounds(self.pos), tags="cell", fill=self.paint_cell())

class Animal(Agent):
	def __init__(self, id, model, age):
		super().__init__(id, model)
		self.kind = ''
		self.age = age
		self.sex = np.random.randint(0, 2)
		self.pregnant = 0
		self.id = id
		self.target = None
		self.pos = (0, 0)
		self.colors = ("#000000", "#000000", "#000000")
		self.canvas = None
		self.food = 0
		self.predicted_lifespan = 9
		self.agility = 1

	def can_mate(self):
		if not self.sex and not self.pregnant and 8 > self.age > 1 and self.food > 50:
			return True
		return False

	def update_speed(self):
		age_ratio = self.age / self.predicted_lifespan
		if age_ratio > 1: age_ratio = 1

		speed_const = -np.power((2 * age_ratio - 1),4) + 1

		self.speed = speed_const * self.agility
		
		if self.pregnant:
			self.speed -= self.pregnant

	def __str__(self):
		return self.kind+' '+str(self.id)

	def update(self):
		self.canvas.itemconfig(self.image, fill=self.colors[self.sex if not self.pregnant else 2])

	def draw(self):
		fill = self.colors[self.sex]
		self.image = self.canvas.create_oval(*get_cell_bounds(self.pos, size=12), fill=fill, tags=self.kind)

	def kill(self):
		self.model.kill(self)

	def step(self):
		self.food -= FOOD_PER_TICK
		self.age += AGE_DELTA
		step = self.model.step_num

		if self.food <= 0:
			print(self, 'died of starvation')
			self.kill()
			return
		if self.age > self.predicted_lifespan:
			print(self, 'died of old age')
			self.kill()
			return

		if self.pregnant:
			self.food -= FOOD_PER_TICK / 3
			self.pregnant += AGE_DELTA
			if self.pregnant >= 1:
				self.pregnant = 0
				self.update()
				babies = perturb_dist(1)
				babies *= (BABIES_PER_DRAGONFLY_PREGNANT if self.kind == 'Dragonfly' else BABIES_PER_MOSQUITO_PREGNANT)
				babies = int(round(babies, 0))
				print(self, "has given birth to", babies, 'babies')
				for _ in range(babies):
					self.model.give_birth(*self.pos, kind=self.kind)

		if not step % 10:
			self.update_speed()

		self.target = self.get_target()
		target = self.target

		if target:
			if not target.pos:
				print("Target has no position!", self, target)
				self.target = None
				return
			
			new_pos = move_to_target(*self.pos, *target.pos, self.speed)
			self.model.space.move_agent(self, new_pos)
			self.canvas.coords(self.image, *get_cell_bounds(new_pos, size=12))

	def get_target(self):

		space = self.model.space
		neighbors = space.get_neighbors(self.pos, radius=3)
		np.random.shuffle(neighbors)

		target = self.target

		if target and target.pos and np.linalg.norm(np.array(self.pos) - np.array(target.pos)) < .5:
			if self.kind == 'Mosquito' and target.kind == 'Grass' and self.food < 80 and target.has_food >= 1:
				target.consume()
				self.food += 10
				return None

			elif self.kind == 'Dragonfly' and target.kind == 'Mosquito' and self.food < 80:
				print(self, 'ate', target)
				self.food += 40 + target.food / 4
				target.kill()
				return None

			elif self.kind == target.kind and target.can_mate():
				print(self, 'mated with', target)
				target.pregnant = 0.1
				target.update()

			else:
				target = None

		if target:
			return target

		if self.food < 80:
			if self.kind == 'Mosquito':
				food_cells = space.get_neighbors(self.pos, radius=RADIUS_MOSQUITO)
				np.random.shuffle(food_cells)
				for element in food_cells:
					if element.kind == 'Grass':
						if element.has_food >= 1:
							return element
			else:
				food_cells = space.get_neighbors(self.pos, radius=RADIUS_DRAGONFLY)
				for element in food_cells:
					if element.kind == 'Mosquito':
						return element

		if self.sex:
			for element in neighbors:
				if self.kind == element.kind and element.can_mate():
					return element

		for element in neighbors:
			if type(element) == Cell and element.kind == 'Grass':
				target = element
				return element


class Dragonfly(Animal):
	def __init__(self, id, model, age=0):
		super().__init__(id, model, age)
		self.kind = 'Dragonfly'
		self.colors = ("#22232b", "#4f536e", "#5d68b3")
		self.agility = 2
		self.predicted_lifespan = perturb_dist(LIFESPAN_DRAGONFLY)
		self.food = 50
		self.update_speed()

class Mosquito(Animal):
	def __init__(self, id, model, age=0):
		super().__init__(id, model, age)
		self.kind = 'Mosquito'
		self.agility = 1
		self.food = 30
		self.predicted_lifespan = perturb_dist(LIFESPAN_MOSQUITO)
		self.colors = ("#f7f2f2", "#e6d7d5", "#d65454")
		self.update_speed()