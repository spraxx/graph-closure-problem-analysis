# Project: Graph Closure Problem Analysis

This project implements and analyzes two algorithms to solve the "k-vertex closure" problem: an exhaustive search and a greedy heuristic.

## Problem
Given a directed graph G(V, E), does G have a closure with k vertices?
A closure is a set of vertices C, such that no edges leave C (i.e., for every node `u` in `C`, all its successors `v` are also in `C`).

## Project Structure

- `requirements.txt`: Python dependencies.
- `graph_generator.py`: Generates and saves graph instances to the `./graphs` directory.
- `algorithms.py`: Contains the implementations of the exhaustive and greedy algorithms.
- `experiment_runner.py`: Runs both algorithms on the generated graphs and saves results to `results.csv`.
- `analysis_report.md`: The final report, including formal complexity analysis and sections for experimental results.
- `graphs/`: Directory where generated graphs are stored.
- `results/`: Directory where experimental results are stored.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create Directories:**
    (Se não existirem)
    ```bash
    mkdir graphs
    mkdir results
    ```

3.  **Generate Graphs:**
    This will generate graphs for `n = 4` to `n = 15`. You can adjust the `MAX_VERTICES` variable inside the script to generate more.
    ```bash
    python src/graph_generator.py
    ```

4.  **Run Experiments:**
    This will run the algorithms on the generated graphs and save the data to `results/results.csv`. This will take time, especially for the exhaustive search on larger graphs.
    ```bash
    python src/experiment_runner.py
    ```
5. **Experiment 2: Large Dese Graphs (Greedy Only)**
    This runs the supplemental test on the Greedy algorithm for n up to 5000+ to test its worst-case performance
    ```bash
    python src/test_large_greedy.py
    ```
6.  **Complete Analysis:**
    Open `analysis_report.md`. Use the `results/results.csv` file (ou o Jupyter Notebook `analise_resultados.ipynb`) to create plots and fill in the sections for your experimental analysis (b, c, d, e).
```