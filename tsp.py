from typing import Tuple, List
from city import City2D
from collections import OrderedDict
# import numpy as np

class TSP:
	def __init__(self, cities_list:List[City2D]) -> None:
		# self.cities = OrderedDict(zip(np.arange(len(cities_list)), cities_list))
		self.cities = OrderedDict(zip(range(len(cities_list)), cities_list))

	def total_distance(self, order:List[int]) -> float:
		distance : float = 0.0

		for i in range(len(order)):
			if i == len(order) - 1:
				curr, succ = self.cities[order[i]], self.cities[order[0]]
			else:
				curr, succ = self.cities[order[i]], self.cities[order[i+1]]

			distance += curr.euclidean_distance(succ)

		return distance

	def get_cities_nums(self) -> List[int]:
		return list(self.cities.keys())

	def get_cities(self) -> List[City2D]:
		return list(self.cities.values())

	def __str__(self) -> str:
		output = "TSP\n" + "-"*30 + "\n"

		for i, c in self.cities.items():
			output += f"{i} -> {c.__str__()}\n"

		return output

	def __repr__(self) -> str:
		return f"TSP({self.get_cities()})"

if __name__ == '__main__':
	from city import City2D

	c1 = City2D(35, "Izmir", 0, 0)
	c2 = City2D(6, "Ankara", 6, 8)
	c3 = City2D(34, "Istanbul", 6, 0)

	tsp = TSP([c1, c2, c3])

	print(tsp)
	print(tsp.__repr__())