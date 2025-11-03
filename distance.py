import math

def euclidean_distance(ax: float, ay: float, bx: float, by: float) -> float:
    """Return Euclidean distance between two points."""
    return math.hypot(bx - ax, by - ay)

def distance(a, b) -> float:
    """
    Accepts pandas Series (with 'x','y') or tuples like (city,x,y) or (x,y).
    Returns float Euclidean distance.
    """
    try:
        ax = float(a["x"]); ay = float(a["y"])
    except Exception:
        if len(a) >= 3:
            ax = float(a[1]); ay = float(a[2])
        else:
            ax = float(a[0]); ay = float(a[1])
    try:
        bx = float(b["x"]); by = float(b["y"])
    except Exception:
        if len(b) >= 3:
            bx = float(b[1]); by = float(b[2])
        else:
            bx = float(b[0]); by = float(b[1])
    return euclidean_distance(ax, ay, bx, by)