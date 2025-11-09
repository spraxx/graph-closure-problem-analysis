import networkx as nx
import time
import random
import os          
import pandas as pd
import algorithms  

RESULTS_DIR = "results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "greedy_dense_results.csv")

def test_large_greedy(n, k, density):
    """
    Gera um grafo aleatório, corre o algoritmo greedy
    e retorna um dicionário de estatísticas detalhadas.
    """
    print(f"--- Testando Instância ---")
    print(f"n = {n}, k = {k}, density = {density}")

    print("A gerar grafo...")
    start_gen = time.perf_counter()
    G = nx.gnp_random_graph(n, density, directed=True)
    gen_time = time.perf_counter() - start_gen
    print(f"Grafo gerado em {gen_time:.4f} segundos (Nós: {G.number_of_nodes()}, Arestas: {G.number_of_edges()})")

    print("A executar find_closure_greedy...")
    (gr_found, gr_closure, gr_stats) = algorithms.find_closure_greedy(G, k)
    algo_time = gr_stats['time']

    total_time = gen_time + algo_time

    print("\n--- Resultados (Greedy) ---")
    print(f"Encontrou Closure: {gr_found}")
    print(f"Tempo Geração:   {gen_time:.6f} segundos")
    print(f"Tempo Algoritmo: {algo_time:.6f} segundos")
    print(f"TEMPO TOTAL:     {total_time:.6f} segundos")
    print(f"Operações Básicas: {gr_stats['basic_ops']}")
    print("---------------------------------\n")

    full_stats = {
        'n': n,
        'k': k,
        'density': density,
        'gen_time': gen_time,
        'algo_time': algo_time,
        'total_time': total_time,
        'basic_ops': gr_stats['basic_ops']
    }
    return full_stats

def main():
    dense_instances = [
        (100, 50, 1.0),   
        (500, 250, 1.0),  
        (1000, 500, 1.0), 
        (1500, 750, 1.0),
        (5000, 2500, 1.0),
        ]

    random_seed = 130449 
    random.seed(random_seed)
    nx.utils.py_random_state(random_seed)
    print(f"Seed aleatória definida para: {random_seed}")
    print("--- A testar instâncias DENSAS (d=1.0) ---") 

    all_stats = []
    
    for n, k, density in dense_instances:
        stats = test_large_greedy(n, k, density)
        all_stats.append(stats)

    print(f"\n--- A guardar resultados em CSV ---")
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Diretório criado: {RESULTS_DIR}")

    df = pd.DataFrame(all_stats)

    df = df[['n', 'k', 'density', 'gen_time', 'algo_time', 'total_time', 'basic_ops']]

    df.to_csv(RESULTS_FILE, index=False)
    print(f"Resultados guardados com sucesso em: {RESULTS_FILE}")
        
    print("\n--- Sumário Final (Testes Densos) ---")

    print(f"{'n':>6} | {'k':>6} | {'Densid.':>7} | {'T. Geração (s)':>15} | {'T. Algo (s)':>12} | {'T. TOTAL (s)':>12} | {'Operações':>10}")
    print("-" * 88)

    for s in all_stats:
        print(f"{s['n']:>6} | {s['k']:>6} | {s['density']:>7.4f} | {s['gen_time']:>15.6f} | {s['algo_time']:>12.6f} | {s['total_time']:>12.6f} | {s['basic_ops']:>10}")

if __name__ == "__main__":
    main()