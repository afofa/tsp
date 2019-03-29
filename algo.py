# from abc import abstractmethod
from typing import List, Callable
from ea import EvolutionaryAgent
from tsp import TSP
import random
from statistics import mean, median

class EvolutionaryAlgorithm:
	def __init__(self, tsp:TSP, agents:List[EvolutionaryAgent]) -> None:
		self.tsp = tsp
		self.agents = agents

	def set_agents(self, agents:List[EvolutionaryAgent]) -> None:
		self.agents = agents

	def get_agents(self) -> List[EvolutionaryAgent]:
		return self.agents

	def _agents_set_default(self) -> None:
		order = self.tsp.get_cities_nums()
		for agent in self.agents:
			agent.set_order(order)

	def _agents_randomly_shuffle(self) -> None:
		for agent in self.agents:
			agent.randomly_shuffle()

	def initialize(self) -> None:
		self._agents_set_default()
		self._agents_randomly_shuffle()

	def fitness(self, transformation_function:Callable[[float], float]=None) -> List[float]:
		def inverse_func(x:float) -> float:
			return 1/x
		def identity_func(x:float) -> float:
			return x

		fitnesses = [self.tsp.total_distance(agent.get_order()) for agent in self.agents]
		if transformation_function is None:
			return list(map(inverse_func, fitnesses))
		else:
			return list(map(inverse_func, fitnesses)), list(map(transformation_function, fitnesses))

	def fitness_to_probability(self, fitnesses:List[float]) -> List[float]:
		def normalization_func(input_list:List[float]) -> List[float]:
			sum_of_input = sum(input_list)
			output_list = [i/sum_of_input for i in input_list]
			return output_list
		return normalization_func(fitnesses)

	def elitism(self, fitnesses:List[float], count:int=1, proportion:float=None) -> List[int]:
		if proportion is not None:
			count = round(len(fitnesses)*proportion)
		sorted_fitnesses_indices = sorted(range(len(fitnesses)), key=fitnesses.__getitem__, reverse=True)
		selected_indices = sorted_fitnesses_indices[:count]
		selected_agents = [self.agents[i] for i in selected_indices]
		return selected_agents

	def select_mating_pool(self, probs:List[float], count:int) -> List[EvolutionaryAgent]:
		mating_pool = random.choices(self.agents, probs, k=count)
		return mating_pool

	def breed(self, mating_pool:List[EvolutionaryAgent], count:int) -> List[EvolutionaryAgent]:
		def breed_two_agents(agent1:EvolutionaryAgent, agent2:EvolutionaryAgent) -> EvolutionaryAgent:
			order1 = agent1.get_order()
			order2 = agent2.get_order()

			length = len(order1)-1

			r1 = random.randint(0, length)
			r2 = random.randint(0, length)
			r1, r2 = min(r1, r2), max(r1, r2)

			part1 = order1[r1:r2+1]
			part2 = order2[r1:r2+1]
			new_order = list(map(lambda i: -1 if i in part1 else i, order2))
			new_order[r1:r2+1] = part1
			replace = list(filter(lambda i: i not in new_order, part2))
			for r in replace:
				index = new_order.index(-1)
				new_order[index] = r

			return EvolutionaryAgent(new_order)

		agents_breed = []
		for i in range(count):
			agent1 = random.choice(mating_pool)
			agent2 = random.choice(mating_pool)
			agents_breed.append(breed_two_agents(agent1, agent2))

		return agents_breed

	def mutation(self, agents:List[EvolutionaryAgent], mutation_prob:float=0.1) -> List[EvolutionaryAgent]:
		for agent in agents:
			new_order = agent.get_order()
			for i in range(len(new_order)):
				if random.random() < mutation_prob:
					i_new = random.randint(0, len(new_order)-1)
					new_order[i], new_order[i_new] = new_order[i_new], new_order[i]
			agent.set_order(new_order)

		return agents

	def next_generation(	self, fitnesses:List[float], 
							elitism_count:int=20, 
							elitism_proportion:float=None,
							mating_pool_count:int=20,
							breed_count:int=80,
							mutation_prob:float=0.1,
							is_set:bool=True) -> List[EvolutionaryAgent]:

			agents_elitism = self.elitism(fitnesses)

			probs = self.fitness_to_probability(fitnesses)
			mating_pool = self.select_mating_pool(probs, mating_pool_count)
			agents_breed = self.breed(mating_pool, breed_count)
			agents_breed = self.mutation(agents_breed, mutation_prob)
			agents_next_generation = agents_elitism + agents_breed

			if is_set:
				self.set_agents(agents_next_generation)

			return agents_next_generation

	def analyze_generation(self, is_verbose:bool=True, is_return_fitnesses:bool=True):
		fitnesses, distances = self.fitness(transformation_function=lambda x: x)
		min_f, max_f, mean_f, median_f = min(fitnesses), max(fitnesses), mean(fitnesses), median(fitnesses)
		min_d, max_d, mean_d, median_d = min(distances), max(distances), mean(distances), median(distances)

		if is_verbose:
			# print(f"min={min_f}\nmax={max_f}\nmean={mean_f}\nmedian={median_f}\n")
			print(f"min={min_d}\nmax={max_d}\nmean={mean_d}\nmedian={median_d}\n")

		if is_return_fitnesses:
			return fitnesses, min_f, max_f, mean_f, median_f
		else:
			return min_f, max_f, mean_f, median_f

	def run_algorithm(self, is_verbose:bool=True, num_of_generations:int=100) -> None:
		self.initialize()

		for i in range(num_of_generations):
			if is_verbose:
				print(f"Generation {i}:")
			fitnesses, _, _, _, _ = self.analyze_generation(is_verbose)
			self.next_generation(fitnesses)
			

if __name__ == '__main__':
	from city import City2D
	from tsp import TSP
	from ea import EvolutionaryAgent

	# c1 = City2D(35, "Izmir", 0, 0)
	# c2 = City2D(6, "Ankara", 6, 8)
	# c3 = City2D(34, "Istanbul", 6, 0)
	# c4 = City2D(9, "Aydin", -2, -3)
	# c5 = City2D(1, "Adana", -7, -12)
	# c6 = City2D(45, "Manisa", 1, 1)
	# c7 = City2D(10, "Balikesir", 12, 14)
	# c8 = City2D(81, "Duzce", 20, 12)

	# cs = [c1, c2, c3, c4, c5, c6, c7, c8]
	num_of_cities = 500
	scale = 200
	cs = [City2D(i, f"City{i}", random.random()*scale, random.random()*scale) for i in range(num_of_cities)]

	tsp = TSP(cs)

	eas = [EvolutionaryAgent() for i in range(100)]

	algo = EvolutionaryAlgorithm(tsp, eas)
	algo.run_algorithm()