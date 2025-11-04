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

2.  **Edit Student Number:**
    Open `graph_generator.py` and `experiment_runner.py` and change the `YOUR_STUDENT_NUMBER` placeholder to your actual student number.

3.  **Create Directories:**
    ```bash
    mkdir graphs
    mkdir results
    ```

4.  **Generate Graphs:**
    This will generate graphs for `n = 4` to `n = 15`. You can adjust the `MAX_VERTICES` variable inside the script to generate more.
    ```bash
    python graph_generator.py
    ```

5.  **Run Experiments:**
    This will run the algorithms on the generated graphs and save the data to `results/results.csv`. This will take time, especially for the exhaustive search on larger graphs.
    ```bash
    python experiment_runner.py
    ```

6.  **Complete Analysis:**
    Open `analysis_report.md`. It already contains the formal complexity analysis. Use the `results/results.csv` file (e.g., by opening it in Excel or using a tool like Pandas/Matplotlib) to create plots and fill in the sections for your experimental analysis (b, c, d, e).
```