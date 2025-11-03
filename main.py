import random
import os
import tsp_parser as parser
import distance as dist
from solution import Solution, random_solution_from_df, solution_from_list

def greedy_tour(df, start_city: int) -> Solution:
    cities_left = set(df["city"].tolist())
    tour = [int(start_city)]
    cities_left.remove(int(start_city))
    current = int(start_city)
    while cities_left:
        cur_row = parser.get_city_row(df, current)
        best = None
        best_d = float("inf")
        for c in cities_left:
            d = dist.distance(cur_row, parser.get_city_row(df, c))
            if d < best_d:
                best_d = d
                best = c
        tour.append(int(best))
        cities_left.remove(best)
        current = int(best)
    return solution_from_list(df, tour)

def greedy_all_starts(df):
    return [(int(s), greedy_tour(df, s)) for s in df["city"].tolist()]

def generate_population(df, n: int, include: list = None, rng=None):
    rng = rng or random.Random()
    pop = []
    if include:
        for s in include:
            pop.append(s)
    while len(pop) < n:
        pop.append(random_solution_from_df(df, rng))
    return pop

def run_for_file(path: str, save_prefix: str = None):
    df = parser.parse_tsp(path)
    # 8. greedy for every start
    all_g = greedy_all_starts(df)
    best_g = min(all_g, key=lambda sb: sb[1].fitness())
    print(f"Best greedy start {best_g[0]} -> {best_g[1].info(name='greedy_best')}")
    # 9. generate 100 random
    rng = random.Random(42)
    rands = [random_solution_from_df(df, rng) for _ in range(100)]
    scores = [s.fitness() for s in rands]
    best_idx = int(min(range(len(scores)), key=lambda i: scores[i]))
    print(rands[best_idx].info(name="random_best"))
    print(f"Random mean {sum(scores)/len(scores):.4f}, min {min(scores):.4f}, max {max(scores):.4f}")
    if save_prefix:
        out = f"{save_prefix}_random_scores.csv"
        with open(out, "w", encoding="utf-8") as w:
            w.write("idx,score\n")
            for i, sc in enumerate(scores):
                w.write(f"{i},{sc:.6f}\n")
        print(f"Saved random scores to {os.path.abspath(out)}")

if __name__ == "__main__":
    # adjust filenames if needed; place these files in project folder
    base = "e:\\py_gen_algorithms\\tsp"
    files = [
        (os.path.join(base, "berlin11_modified.tsp"), os.path.join(base, "berlin11")),
        (os.path.join(base, "berlin52.tsp"), os.path.join(base, "berlin52")),
    ]
    for path, prefix in files:
        if not os.path.exists(path):
            print(f"File not found: {path}  (put the .tsp file in e:\\py_gen_algorithms)")
            continue
        print(f"\n--- Running for {path} ---")
        # do not save CSV results: call without save_prefix (or pass None)
        run_for_file(path)