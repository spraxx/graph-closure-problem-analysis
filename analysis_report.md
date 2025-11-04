# Analysis of Algorithms for the k-Vertex Closure Problem

**Project:** Exhaustive vs. Greedy Algorithms for the k-Vertex Closure Problem
**Problem:** For a given directed graph G(V, E), does G have a closure with k vertices?
**Student Seed:** `123456` (Replace with your number)

---

## a) Formal Computational Complexity Analysis

### 1. Exhaustive Search Algorithm (`find_closure_exhaustive`)

The algorithm operates in two main phases:
1.  **Combination Generation:** It generates all possible subsets (combinations) of vertices `C` of size `k` from the set of `n` vertices `V`. The number of such combinations is given by "n choose k", or $\binom{n}{k}$.
2.  **Closure Verification:** For each generated combination `C`, it calls `check_is_closure`.

The `check_is_closure(G, C)` function iterates through each vertex `u` in the set `C` (which has `k` vertices). For each `u`, it iterates through all its successors `v`. In the worst case, a vertex `u` can have an out-degree of $O(n)$.

-   **Worst-Case Verification:** The check for a single combination `C` involves iterating over `k` nodes. The total number of edges checked is the sum of out-degrees for all nodes in `C`. This can be bounded by $O(k \times n)$ (in a dense graph) or $O(m)$ (where `m` is the total number of edges in `G`). A simpler bound is $O(k \times \text{max\_out\_degree}) = O(k \times n)$.

-   **Total Complexity:** The total complexity is the number of combinations multiplied by the cost of verifying each one.
    $$T(n, k) = O(\binom{n}{k} \times (k \times n))$$

    Since $\binom{n}{k}$ is $O(n^k)$, the complexity can be expressed as:
    $$T(n, k) = O(n^k \times k \times n) = O(k \times n^{k+1})$$

    If `k` is not fixed and depends on `n` (e.g., $k = n/2$), then $\binom{n}{n/2}$ is $O(\frac{2^n}{\sqrt{n}})$. This shows the algorithm is **exponential in `n`**.

### 2. Greedy Heuristic Algorithm (`find_closure_greedy`)

This algorithm works by starting with the set of all vertices `C = V` and iteratively removing nodes.
1.  **Outer Loop:** The algorithm needs to remove $n - k$ vertices to reach the target size `k`. This loop runs $O(n)$ times.
2.  **Inner Work:** Inside the loop, it must find a node `u` in `C` that has an in-degree of 0 *relative to other nodes in C*.
    -   Our implementation creates a subgraph view: `subgraph = G.subgraph(C)`. This operation in NetworkX is efficient, but in the worst-case, it can take up to $O(n^2)$ to build the subgraph representation.
    -   It then iterates through all nodes `u` in `C` (up to $O(n)$ nodes).
    -   For each `u`, it checks `subgraph.in_degree(u)`. This check is $O(\text{avg\_degree\_in\_subgraph})$ or $O(n)$ in the worst case.
    -   The total cost of the inner work (finding a node to remove) is $O(n^2)$ (for subgraph creation) + $O(n^2)$ (for iterating and checking degrees) = $O(n^2)$.

-   **Total Complexity:** The total complexity is the cost of the outer loop multiplied by the cost of the inner work.
    $$T(n, k) = O(n \times n^2) = O(n^3)$$

    This algorithm is **polynomial in `n`**, which is vastly more efficient than the exponential exhaustive search.

---

## b) Experimental Analysis

(You must run `experiment_runner.py` to get `results.csv` and use that data to complete this section)

### 1. Number of Basic Operations
-   **Exhaustive:** Plot `ex_basic_ops` vs. `n` (using different colors/lines for each density).
-   **Greedy:** Plot `gr_basic_ops` vs. `n` (using different colors/lines for each density).

*(Paste your plots or describe your findings here)*
*Example description:* "The number of operations for the exhaustive search grew extremely fast, consistent with an exponential curve. The operations for the greedy algorithm grew much slower, appearing polynomial (likely cubic, as predicted)."

### 2. Execution Time
-   **Exhaustive:** Plot `ex_time_sec` vs. `n`.
-   **Greedy:** Plot `gr_time_sec` vs. `n`.
-   You may want to use a **logarithmic scale** for the y-axis on the exhaustive plot to make it readable.

*(Paste your plots or describe your findings here)*
*Example description:* "The execution time for the exhaustive search exploded, becoming unusable after n=14. The greedy algorithm's time remained under 1 second for all tested instances."

### 3. Number of Solutions / Configurations Tested
-   This applies mainly to the exhaustive search.
-   Plot `ex_solutions_tested` vs. `n`.
-   Compare this plot to the theoretical values of $\binom{n}{k}$ (where $k = n // 2$).

*(Paste your plots or describe your findings here)*
*Example description:* "The number of solutions tested was identical to the formula for $\binom{n}{n // 2}$, confirming the algorithm's exhaustive nature."

### 4. Precision (Recall) of the Greedy Heuristic
-   Filter the `results.csv` data for rows where `ex_found == True`.
-   From that subset, calculate the percentage where `gr_found == True`. This is the **Recall**.
-   Analyze if the recall changes with `n` or `density`.

*(Paste your calculations or describe your findings here)*
*Example description:* "The greedy heuristic's recall was analyzed. Of the `X` total instances where a closure existed, the greedy algorithm successfully found one `Y` times, for a total recall of `(Y/X) * 100`%. It was observed that the recall was lower for denser graphs, as this created fewer opportunities for nodes to have an in-degree of 0."

---

## c) Comparison of Experimental and Formal Analysis

-   Compare your plots from (b) with the formal analysis from (a).
-   Does the exhaustive search plot *look* exponential?
-   Does the greedy search plot *look* polynomial (e.g., cubic, $O(n^3)$)?
-   You can test this by plotting `log(time)` vs. `n` (which should be roughly linear for an exponential algorithm) and `log(time)` vs. `log(n)` (which should be linear with a slope of ~3 for a cubic algorithm).

*(Write your comparison here)*
*Example description:* "The experimental results strongly support the formal analysis. A plot of log(time) vs. n for the exhaustive search was nearly a straight line, confirming exponential growth. A plot of log(time) vs. log(n) for the greedy algorithm showed a linear relationship with a slope of approximately 2.8, closely matching the predicted $O(n^3)$ complexity."

---

## d) Largest Graph for Exhaustive Search

-   Define "too much time". Let's use a 60-second limit.
-   Look at your `results.csv` data.
-   Find the largest value of `n` for which the `ex_time_sec` was consistently below 60 seconds across all densities.

*(Write your finding here)*
*Example finding:* "Using a 60-second limit, the largest graph my computer could process with the exhaustive search was **n = 14**. At n = 15, the 50% density graph took 112 seconds."

---

## e) Estimation for Larger Instances

-   Use your data from (b) to extrapolate.
-   **Exhaustive:**
    -   Find the ratio of times, e.g., $T(n=14) / T(n=13)$.
    -   Estimate $T(n=20) \approx T(n=14) \times (\text{ratio})^6$.
-   **Greedy:**
    -   Find the ratio $T(n=14) / T(n=13)$. It should be close to $(14/13)^3$.
    -   Estimate $T(n=100) \approx T(n=14) \times (100/14)^3$.

*(Write your estimates here)*
*Example estimation:*
-   **Exhaustive:** "The time for n=13 was ~20s and n=14 was ~55s (a factor of ~2.75). To estimate for `n = 20` (6 more steps), we get $55 \times (2.75)^6 \approx 55 \times 475 \approx 26,125$ seconds, or **~7.25 hours**."
-   **Greedy:** "The time for n=14 was ~0.005s. To estimate for `n = 1000`, we use the $O(n^3)$ model: $T(1000) \approx T(14) \times (1000 / 14)^3 \approx 0.005s \times (71.4)^3 \approx 0.005 \times 364,500 \approx 1822$ seconds, or **~30 minutes**."
