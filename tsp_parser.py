import re
from typing import List, Tuple
import pandas as pd

def parse_tsp(file_path: str) -> pd.DataFrame:
    """
    Parse a .tsp file and return DataFrame with columns: city (int), x (float), y (float)
    Stops at EOF or end of NODE_COORD_SECTION.
    """
    coords: List[Tuple[int, float, float]] = []
    in_section = False
    number_re = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

    with open(file_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.upper().startswith("NODE_COORD_SECTION"):
                in_section = True
                continue
            if not in_section:
                continue
            if line.upper().startswith("EOF"):
                break
            tokens = number_re.findall(line)
            if len(tokens) < 3:
                continue
            city = int(float(tokens[0]))
            x = float(tokens[1])
            y = float(tokens[2])
            coords.append((city, x, y))

    if not coords:
        raise ValueError(f"No coordinates found in {file_path}")

    df = pd.DataFrame(coords, columns=["city", "x", "y"])
    df = df.sort_values("city").reset_index(drop=True)
    df = df.astype({"city": int, "x": float, "y": float})
    return df

def get_city_row(df: pd.DataFrame, city_id: int) -> pd.Series:
    sel = df[df["city"] == int(city_id)]
    if sel.empty:
        raise KeyError(f"City id {city_id} not found")
    return sel.iloc[0]