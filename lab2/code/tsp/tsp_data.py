"""
TSP Dataset Handler
Download and parse TSP datasets from TSPLIB format
"""

import math
import re
from typing import List, Tuple, Dict
import urllib.request


class TSPDataset:
    """Handle TSP dataset loading and parsing"""
    
    def __init__(self):
        self.name = ""
        self.dimension = 0
        self.edge_weight_type = ""
        self.coordinates = []  # List of (x, y) tuples
        self.cities = []  # List of city indices
    
    def load_from_file(self, filename: str):
        """Load TSP data from file"""
        with open(filename, 'r') as f:
            content = f.read()
        
        self._parse_tsp_data(content)
    
    def load_from_string(self, content: str):
        """Load TSP data from string"""
        self._parse_tsp_data(content)
    
    def _parse_tsp_data(self, content: str):
        """Parse TSPLIB format data"""
        lines = content.strip().split('\n')
        
        in_coord_section = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('NAME'):
                self.name = line.split(':')[1].strip()
            elif line.startswith('DIMENSION'):
                self.dimension = int(line.split(':')[1].strip())
            elif line.startswith('EDGE_WEIGHT_TYPE'):
                self.edge_weight_type = line.split(':')[1].strip()
            elif line == 'NODE_COORD_SECTION':
                in_coord_section = True
            elif line == 'EOF':
                break
            elif in_coord_section and line:
                parts = line.split()
                if len(parts) >= 3:
                    city_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    self.cities.append(city_id - 1)  # 0-indexed
                    self.coordinates.append((x, y))
    
    def calculate_distance(self, city1: int, city2: int) -> float:
        """Calculate distance between two cities"""
        x1, y1 = self.coordinates[city1]
        x2, y2 = self.coordinates[city2]
        
        if self.edge_weight_type == 'EUC_2D':
            # Euclidean distance
            dx = x1 - x2
            dy = y1 - y2
            return math.sqrt(dx * dx + dy * dy)
        
        elif self.edge_weight_type == 'GEO':
            # Geographic distance
            PI = 3.141592
            deg = int(x1)
            min_val = x1 - deg
            lat1 = PI * (deg + 5.0 * min_val / 3.0) / 180.0
            
            deg = int(y1)
            min_val = y1 - deg
            lon1 = PI * (deg + 5.0 * min_val / 3.0) / 180.0
            
            deg = int(x2)
            min_val = x2 - deg
            lat2 = PI * (deg + 5.0 * min_val / 3.0) / 180.0
            
            deg = int(y2)
            min_val = y2 - deg
            lon2 = PI * (deg + 5.0 * min_val / 3.0) / 180.0
            
            RRR = 6378.388
            q1 = math.cos(lon1 - lon2)
            q2 = math.cos(lat1 - lat2)
            q3 = math.cos(lat1 + lat2)
            return int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
        
        else:
            # Default to Euclidean
            dx = x1 - x2
            dy = y1 - y2
            return math.sqrt(dx * dx + dy * dy)
    
    def calculate_tour_length(self, tour: List[int]) -> float:
        """Calculate total length of a tour"""
        total_distance = 0
        
        for i in range(len(tour)):
            city1 = tour[i]
            city2 = tour[(i + 1) % len(tour)]
            total_distance += self.calculate_distance(city1, city2)
        
        return total_distance
    
    def get_distance_matrix(self) -> List[List[float]]:
        """Pre-compute distance matrix for faster access"""
        n = self.dimension
        matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = self.calculate_distance(i, j)
                matrix[i][j] = dist
                matrix[j][i] = dist
        
        return matrix


def create_sample_dataset(n_cities: int = 10) -> TSPDataset:
    """Create a small random TSP dataset for testing"""
    import random
    
    dataset = TSPDataset()
    dataset.name = f"Random_{n_cities}"
    dataset.dimension = n_cities
    dataset.edge_weight_type = "EUC_2D"
    
    random.seed(42)
    for i in range(n_cities):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        dataset.cities.append(i)
        dataset.coordinates.append((x, y))
    
    return dataset


# Sample TSP datasets (small ones for testing)
SAMPLE_TSP_DATA = {
    "burma14": """NAME: burma14
TYPE: TSP
COMMENT: 14-Staedte in Burma (Zaw Win)
DIMENSION: 14
EDGE_WEIGHT_TYPE: GEO
NODE_COORD_SECTION
1 16.47 96.10
2 16.47 94.44
3 20.09 92.54
4 22.39 93.37
5 25.23 97.24
6 22.00 96.05
7 20.47 97.02
8 17.20 96.29
9 16.30 97.38
10 14.05 98.12
11 16.53 97.38
12 21.52 95.59
13 19.41 97.13
14 20.09 94.55
EOF
""",
    
    "ulysses16": """NAME: ulysses16.tsp
TYPE: TSP
COMMENT: Odyssey of Ulysses (Groetschel/Padberg)
DIMENSION: 16
EDGE_WEIGHT_TYPE: GEO
NODE_COORD_SECTION
1 38.24 20.42
2 39.57 26.15
3 40.56 25.32
4 36.26 23.12
5 33.48 10.54
6 37.56 12.19
7 38.42 13.11
8 37.52 20.44
9 41.23 9.10
10 41.17 13.05
11 36.08 -5.21
12 38.47 15.13
13 38.15 15.35
14 37.51 15.17
15 35.49 14.32
16 39.36 19.56
EOF
"""
}


def load_sample_dataset(name: str) -> TSPDataset:
    """Load a sample dataset"""
    if name in SAMPLE_TSP_DATA:
        dataset = TSPDataset()
        dataset.load_from_string(SAMPLE_TSP_DATA[name])
        return dataset
    else:
        raise ValueError(f"Unknown dataset: {name}")


if __name__ == "__main__":
    # Test dataset loading
    print("Testing TSP Dataset Loader")
    print("=" * 60)
    
    # Test sample datasets
    for name in SAMPLE_TSP_DATA.keys():
        print(f"\nDataset: {name}")
        dataset = load_sample_dataset(name)
        print(f"Dimension: {dataset.dimension}")
        print(f"Type: {dataset.edge_weight_type}")
        print(f"First 3 cities: {dataset.coordinates[:3]}")
        
        # Test tour length calculation
        simple_tour = list(range(dataset.dimension))
        length = dataset.calculate_tour_length(simple_tour)
        print(f"Simple tour (0,1,2,...) length: {length:.2f}")
    
    # Test random dataset
    print("\n\nRandom Dataset:")
    random_dataset = create_sample_dataset(10)
    print(f"Dimension: {random_dataset.dimension}")
    print(f"Coordinates: {random_dataset.coordinates}")
    simple_tour = list(range(10))
    print(f"Simple tour length: {random_dataset.calculate_tour_length(simple_tour):.2f}")
