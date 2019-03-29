from typing import List
import random
# import numpy as np

class EvolutionaryAgent:
	def __init__(self, order:List[int]=None) -> None:
		self.order = order

	def set_order(self, order:List[int]) -> None:
		self.order = order

	def get_order(self) -> List[int]:
		return self.order

	def randomly_shuffle(self) -> None:
		random_order = random.sample(self.order, len(self.order))
		self.set_order(random_order)

	def __str__(self) -> str:
		return f"EA ({self.order})"