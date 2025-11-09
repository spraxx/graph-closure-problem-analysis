import networkx as nx
import numpy as np
import random
import os
import math

# --- CONFIGURATION ---
STUDENT_ID = 130449
MIN_DIST = 5.0
COORD_MIN = 1
COORD_MAX = 500
MAX_VERTICES = 16
DENSITIES = [0.125, 0.25, 0.50, 0.75]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

GRAPH_DIR = os.path.join(PROJECT_ROOT, "graphs")

def set_seed(seed):
    """Sets the random seed for all necessary libraries."""
    random.seed(seed)
    np.random.seed(seed)
    print(f"Random seed set to: {seed}")

def get_dist(p1, p2):
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def generate_vertices(n):
    """Generates n 2D vertices, ensuring they are not too close."""
    points = set()
    attempts = 0
    max_attempts = n * 1000  # Safety break

    while len(points) < n and attempts < max_attempts:
        x = random.randint(COORD_MIN, COORD_MAX)
        y = random.randint(COORD_MIN, COORD_MAX)
        new_point = (x, y)

        if new_point in points:
            attempts += 1
            continue

        is_too_close = False
        for p in points:
            if get_dist(new_point, p) < MIN_DIST:
                is_too_close = True
                break
        
        if not is_too_close:
            points.add(new_point)
        
        attempts += 1
    
    if len(points) < n:
        raise Exception(f"Could not generate {n} vertices with min_dist={MIN_DIST}. Try a smaller min_dist or larger coordinate range.")

    return list(points)

def generate_graphs(n, vertices):
    """Generates graphs for a given n and set of vertices at different densities."""
    graphs = []
    max_edges = n * (n - 1)
    nodes = list(vertices)

    for density in DENSITIES:
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        
        num_edges = int(max_edges * density)
        edges_added = 0

        while edges_added < num_edges:
            u = random.choice(nodes)
            v = random.choice(nodes)

            if u != v and not G.has_edge(u, v):
                G.add_edge(u, v)
                edges_added += 1
        
        graphs.append((density, G))
    return graphs

def main():
    if not os.path.exists(GRAPH_DIR):
        os.makedirs(GRAPH_DIR)
        print(f"Created directory: {GRAPH_DIR}")

    set_seed(STUDENT_ID)
    
    for n in range(4, MAX_VERTICES + 1):
        print(f"--- Generating graphs for n = {n} ---")
        try:
            vertices = generate_vertices(n)
            generated_graphs = generate_graphs(n, vertices)
            
            for density, G in generated_graphs:
                density_str = str(int(density * 100))
                filename = f"{GRAPH_DIR}/graph_n{n}_d{density_str}.gml"
                nx.write_gml(G, filename)
                print(f"  Saved graph to {filename} (Edges: {G.number_of_edges()})")
                
        except Exception as e:
            print(f"Failed to generate graphs for n = {n}: {e}")
            break

    print("--- Graph generation complete. ---")

if __name__ == "__main__":
    main()
