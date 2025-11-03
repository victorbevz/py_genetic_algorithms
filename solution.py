from dataclasses import dataclass
from typing import List, Iterable, Optional
import random
import pandas as pd

import tsp_parser as parser
import distance as dist

@dataclass
class Solution:
    tour: List[int]
    df: Optional[pd.DataFrame] = None  

    def __post_init__(self):
        self.tour = [int(x) for x in self.tour]

    def verify(self) -> bool:
        if self.df is None:
            return True
        city_set = set(self.df["city"].tolist())
        tour_set = set(self.tour)
        return len(self.tour) == len(city_set) and tour_set == city_set

    def fitness(self, close_tour: bool = True) -> float:
        if self.df is None:
            raise RuntimeError("df not set for Solution.fitness")
        total = 0.0
        for a, b in zip(self.tour, self.tour[1:]):
            total += dist.distance(parser.get_city_row(self.df, a), parser.get_city_row(self.df, b))
        if close_tour and len(self.tour) >= 2:
            total += dist.distance(parser.get_city_row(self.df, self.tour[-1]), parser.get_city_row(self.df, self.tour[0]))
        return float(total)

    def info(self, name: Optional[str] = None, close_tour: bool = True) -> str:
        score = self.fitness(close_tour=close_tour)
        prefix = f"[{name}] " if name else ""
        tour_s = " ".join(str(x) for x in self.tour)
        return f"{prefix}{tour_s}  score: {score:.4f}"

def random_solution_from_df(df: pd.DataFrame, rng: Optional[random.Random] = None) -> Solution:
    rng = rng or random
    ids = df["city"].tolist()
    perm = ids[:] 
    rng.shuffle(perm)
    sol = Solution(perm, df=df)
    assert sol.verify()
    return sol

def solution_from_list(df: pd.DataFrame, lst: Iterable[int]) -> Solution:
    sol = Solution(list(lst), df=df)
    assert sol.verify()
    return sol