from typing import List, Tuple
# import numpy as np

class City2D:
	def __init__(self, city_id:int, city_name:str, x:float, y:float) -> None:
		self.city_id = city_id
		self.city_name = city_name
		self.x = x
		self.y = y

	def coordinates(self) -> Tuple[float, float]:
		return self.x, self.y

	def euclidean_distance(self, other_city) -> float:
	# def euclidean_distance(self, other_city:City2D) -> float:	
		x0, y0 = self.coordinates()
		x1, y1 = other_city.coordinates()

		# distance = np.sqrt((x0-x1)**2 + (y0-y1)**2)
		distance = ((x0-x1)**2 + (y0-y1)**2) ** (0.5)

		return distance

	def __str__(self) -> str:
		return f"{self.city_id}. {self.city_name} ({self.x}, {self.y})"

	def __repr__(self) -> str:
		return f"City2D({self.city_id},{self.city_name},{self.x},{self.y})"

if __name__ == '__main__':
	c1 = City2D(35, "Izmir", 0, 0)
	c2 = City2D(6, "Ankara", 6, 8)
	c3 = City2D(34, "Istanbul", 6, 0)

	print(c1)
	print(c2.__repr__())
	print(c1.euclidean_distance(c2))