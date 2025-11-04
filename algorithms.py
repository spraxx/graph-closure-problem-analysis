import networkx as nx
import itertools
import time

def check_is_closure(G: nx.DiGraph, C: set) -> tuple[bool, int]:
    """
    Checks if a set of vertices C is a closure in graph G.
    Returns (is_closure, basic_operations)
    """
    basic_ops = 0
    if not C:
        return True, 0  # An empty set is trivially a closure

    for u in C:
        # A basic operation can be defined as checking a node's successors
        basic_ops += 1
        for v in G.successors(u):
            # An alternative basic_op: count each edge traversal
            # basic_ops += 1
            if v not in C:
                return False, basic_ops  # Found an edge leaving C
    
    return True, basic_ops

def find_closure_exhaustive(G: nx.DiGraph, k: int) -> tuple[bool, set | None, dict]:
    """
    Finds a closure of size k using an exhaustive search.
    
    Returns:
        (bool): True if a closure was found.
        (set | None): The closure set if found, else None.
        (dict): A dictionary of statistics.
    """
    start_time = time.perf_counter()
    nodes = list(G.nodes())
    n = len(nodes)
    
    if k < 0 or k > n:
        stats = {"time": 0, "solutions_tested": 0, "basic_ops": 0}
        return False, None, stats

    if k == 0:
        stats = {"time": time.perf_counter() - start_time, "solutions_tested": 1, "basic_ops": 0}
        return True, set(), stats

    solutions_tested = 0
    total_basic_ops = 0

    # 1. Generate all combinations of size k
    for C_tuple in itertools.combinations(nodes, k):
        C = set(C_tuple)
        solutions_tested += 1
        
        # 2. Check if the combination is a closure
        is_closure, basic_ops = check_is_closure(G, C)
        total_basic_ops += basic_ops
        
        if is_closure:
            end_time = time.perf_counter()
            stats = {
                "time": end_time - start_time,
                "solutions_tested": solutions_tested,
                "basic_ops": total_basic_ops
            }
            return True, C, stats # Found one!
            
    # 3. If loop finishes, no closure was found
    end_time = time.perf_counter()
    stats = {
        "time": end_time - start_time,
        "solutions_tested": solutions_tested,
        "basic_ops": total_basic_ops
    }
    return False, None, stats

def find_closure_greedy(G: nx.DiGraph, k: int) -> tuple[bool, set | None, dict]:
    """
    Tries to find a closure of size k using a greedy heuristic.
    
    Heuristic: Start with the full graph (which is a closure) and
    greedily remove nodes with an in-degree of 0 *within the 
    current closure set C* until C has size k.
    
    Returns:
        (bool): True if a closure of size k was found.
        (set | None): The closure set if found, else None.
        (dict): A dictionary of statistics.
    """
    start_time = time.perf_counter()
    nodes = set(G.nodes())
    n = len(nodes)
    total_basic_ops = 0
    
    if k < 0 or k > n:
        stats = {"time": 0, "basic_ops": 0}
        return False, None, stats
    
    if k == 0:
        stats = {"time": time.perf_counter() - start_time, "basic_ops": 0}
        return True, set(), stats

    C = set(G.nodes())
    
    while len(C) > k:
        # Find a node in C with in-degree 0 *from other nodes in C*
        node_to_remove = None
        
        # We can optimize this by finding all nodes to remove in one go
        # A basic operation could be the check of a node's in-degree
        
        # Create a subgraph view for efficient degree checks
        # This is a bit expensive, but correct.
        subgraph = G.subgraph(C)
        total_basic_ops += 1 # Count subgraph creation as an operation
        
        for u in C:
            total_basic_ops += 1 # Count degree check as an operation
            if subgraph.in_degree(u) == 0:
                node_to_remove = u
                break # Found one, greedy choice
        
        if node_to_remove:
            C.remove(node_to_remove)
        else:
            # Heuristic is "stuck". No node can be removed.
            # We failed to find a closure of size k.
            end_time = time.perf_counter()
            stats = {"time": end_time - start_time, "basic_ops": total_basic_ops}
            return False, C, stats

    # If we exit the loop, len(C) must be k
    end_time = time.perf_counter()
    stats = {"time": end_time - start_time, "basic_ops": total_basic_ops}
    
    if len(C) == k:
        return True, C, stats
    else:
        # This case should not be reachable due to the 'stuck' check
        return False, C, stats
