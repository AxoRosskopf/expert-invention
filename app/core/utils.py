import re
import math
from typing import List

def from_map_url_to_coordinates(url: str) -> List[float]:
    print(f"Parsing URL for coordinates: {url}")
    pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
    match_at = re.search(pattern, url)
    if match_at:
        return [float(match_at.group(1)), float(match_at.group(2))]
    
    return [1e10, 1e10]

def haversine_distance(coord1: List[float], coord2: List[float]) -> float:
    if coord1 == [1e10, 1e10] or coord2 == [1e10, 1e10]:
        return float('inf')
    R = 6371.0
    lat1_rad , lon1_rad = math.radians(coord1[0]), math.radians(coord1[1])
    lat2_rad , lon2_rad = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance