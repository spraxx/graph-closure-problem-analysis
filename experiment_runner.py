import networkx as nx
import os
import pandas as pd
from tqdm import tqdm  # For a nice progress bar

import algorithms

# --- CONFIGURATION ---
STUDENT_ID = 130449

GRAPH_DIR = "graphs"
RESULTS_DIR = "results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.csv")
MAX_VERTICES = 15 # Must match graph_generator.py
DENSITIES = [0.125, 0.25, 0.50, 0.75]
# --- END CONFIGURATION ---

def main():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    results_data = []
    
    # Set up the loop with tqdm for progress
    n_range = list(range(4, MAX_VERTICES + 1))
    pbar = tqdm(n_range, desc="Processing n")
    
    for n in pbar:
        # We will test for k = n/2 (rounded down)
        # This is often a hard case for exhaustive search
        k = n // 2
        pbar.set_postfix_str(f"k={k}")
        
        for density in DENSITIES:
            density_str = str(int(density * 100))
            filename = f"{GRAPH_DIR}/graph_n{n}_d{density_str}.gml"
            
            if not os.path.exists(filename):
                print(f"Warning: Graph file not found, skipping: {filename}")
                continue
                
            G = nx.read_gml(filename, label="label") # Use 'label' to read string labels if any
            
            # --- Run Exhaustive Search ---
            (ex_found, ex_closure, ex_stats) = algorithms.find_closure_exhaustive(G, k)
            
            # --- Run Greedy Heuristic ---
            (gr_found, gr_closure, gr_stats) = algorithms.find_closure_greedy(G, k)
            
            # --- Calculate Heuristic Precision/Recall ---
            # Precision = TP / (TP + FP)
            # Recall = TP / (TP + FN)
            # TP (True Positive): ex_found=True, gr_found=True
            # FP (False Positive): ex_found=False, gr_found=True
            # FN (False Negative): ex_found=True, gr_found=False
            
            # Our greedy algorithm is sound: it only returns True if it finds a
            # *valid* closure. So, FP will always be 0.
            # Precision = TP / (TP + 0) = 1.0 (if TP > 0)
            # We will measure "Recall" (Sensitivity) instead, which is more interesting:
            # "Of the times a solution existed, did the greedy algo find it?"
            recall = None
            if ex_found:
                recall = 1.0 if gr_found else 0.0

            # Store results
            results_data.append({
                "n": n,
                "k": k,
                "density": density,
                "max_edges": n * (n - 1),
                "edges": G.number_of_edges(),
                "ex_found": ex_found,
                "ex_time_sec": ex_stats["time"],
                "ex_basic_ops": ex_stats["basic_ops"],
                "ex_solutions_tested": ex_stats["solutions_tested"],
                "gr_found": gr_found,
                "gr_time_sec": gr_stats["time"],
                "gr_basic_ops": gr_stats["basic_ops"],
                "heuristic_recall": recall
            })

    # Save all results to a CSV file
    df = pd.DataFrame(results_data)
    df.to_csv(RESULTS_FILE, index=False)
    
    print(f"\n--- Experiment complete! ---")
    print(f"Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
