import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd

# -----------------------------------------------------------------------------------

# Funções auxiliares 

def check_dominante(dominante, G):
    dominados = set(dominante)
    for v in dominante:
        dominados.update(G.neighbors(v))
    return dominados == set(G.nodes)

def melhoria_local(dominante, G):
    improved = True
    while improved:
        improved = False
        for u in list(dominante):
            for v in (set(G.nodes) - dominante):
                novo_dominante = (dominante - {u}) | {v}
                if check_dominante(novo_dominante, G) and len(novo_dominante) < len(dominante):
                    dominante = novo_dominante
                    improved = True
                    break
            if improved:
                break
    return dominante

def seleciona_vertice_pra_deletar_aleatorio(D):
    return random.choice(list(D))

def seleciona_maior_dominante(D, G):
    undominated = set(G.nodes) - {v for u in D for v in G.neighbors(u)}
    best_vertex = max(undominated, key=lambda v: len(set(G.neighbors(v)) - D))
    return best_vertex

# -----------------------------------------------------------------------------------

# Inserção Inicial Gulosa (GIP)
def insercao_inicial_gulosa(G):
    v_folhas = {v for v in G.nodes if len(list(G.neighbors(v))) == 1}
    v_suporte = {u for v in v_folhas for u in G.neighbors(v)}

    dominante = v_suporte.copy()

    def gGIP(v, dominant):
        N_v = set(G.neighbors(v)) | {v}
        N_dominantes = set(neighbor for u in dominant for neighbor in G.neighbors(u)) | dominant
        return len(N_v - N_dominantes)

    while not check_dominante(dominante, G):
        candidates = (v for v in G.nodes if v not in dominante and v not in v_folhas)
        v_best = max(candidates, key=lambda v: gGIP(v, dominante))
        dominante.add(v_best)
    return dominante

# Exclusão Inicial Gulosa (GDP)
def exclusao_inicial_gulosa(G):
    dominante = set(G.nodes)
    
    def gGDP(v, dominant):
        return sum(1 for neighbor in G.neighbors(v) if all(neighbor not in G.neighbors(u) for u in (dominant - {v})))
    
    while check_dominante(dominante, G):
        v_best = min(dominante, key=lambda v: gGDP(v, dominante))
        dominante.remove(v_best)
        if not check_dominante(dominante, G):
            dominante.add(v_best)
            break
    return dominante

# Funções de Destruição
def destruicao(D, beta):
    D_d = D.copy()
    num_to_remove = int(beta * len(D))
    for _ in range(num_to_remove):
        v = seleciona_vertice_pra_deletar_aleatorio(D_d)
        D_d.remove(v)
    return D_d

def destruicao_gulosa(dominant, G, beta):
    num_to_remove = int(beta * len(dominant))
    
    def vertex_contribution(v, dominant):
        return sum(
            any(neighbor in G.neighbors(w) for w in (dominant - {v})) for neighbor in G.neighbors(v)
        )
    
    vertices_sorted = sorted(dominant, key=lambda v: vertex_contribution(v, dominant))
    
    for v in vertices_sorted[:num_to_remove]: 
        dominant.remove(v)
    
    return dominant

# Função de Reconstrução
def reconstrucao(dominante_v_deletado, G):
    dominante_reconstruido = dominante_v_deletado.copy()
    while not check_dominante(dominante_reconstruido, G):
        # Seleciona o vértice a ser adicionado
        v = seleciona_maior_dominante(dominante_reconstruido, G)
        
        # Verifica se o vértice selecionado já está no conjunto
        if v not in dominante_reconstruido:
            dominante_reconstruido.add(v)
        else:
            print(f"Vértice {v} já está no conjunto dominante.")
            break  # Evita loop infinito se a função não encontrar um vértice válido
        
        # Depuração: Verificar o estado do conjunto dominante
        print(f"Dominante reconstruído: {dominante_reconstruido}")
        
    return dominante_reconstruido

# Algoritmo IG
def IG(G, beta, delta_max, init_method, destruction_method):
    if init_method == 'GIP':
        dominante = insercao_inicial_gulosa(G)
    elif init_method == 'GDP':
        dominante = exclusao_inicial_gulosa(G)
    
    dominante_melhorado = melhoria_local(dominante, G)
    delta = 0

    while delta < delta_max:
        if destruction_method == destruicao_gulosa:
            dominante_v_deletado = destruicao_gulosa(dominante_melhorado, G, beta)
            print("SSSSSSSSSSSSSSSSSS")
        else:
            dominante_v_deletado = destruicao(dominante_melhorado, beta)
            print("AAAAAAAAAAAAA")
            print(dominante_v_deletado)

        dominante_reconstruido = reconstrucao(dominante_v_deletado, G)
        print("aaa")
        dominante_ideal = melhoria_local(dominante_reconstruido, G)

        if len(dominante_ideal) < len(dominante_melhorado):
            dominante_melhorado = dominante_ideal
            delta = 0
        else:
            delta += 1
    return dominante_melhorado

if __name__ == '__main__':
    G = nx.erdos_renyi_graph(15, 0.3)
    beta = 0.2
    delta_max = 10

    scenarios = [
        ('GIP', destruicao),
        ('GIP', destruicao_gulosa),
        ('GDP', destruicao),
        ('GDP', destruicao_gulosa)
    ]
    
    fig, axes = plt.subplots(len(scenarios), 3, figsize=(15, 5 * len(scenarios)))
    pos = nx.spring_layout(G)
    
    results = []
    
    for i, (init_method, destruction_method) in enumerate(scenarios):
        if init_method == 'GIP':
            D_initial = insercao_inicial_gulosa(G)
        elif init_method == 'GDP':
            D_initial = exclusao_inicial_gulosa(G)

        D_final = IG(G, beta, delta_max, init_method, destruction_method)

        results.append((init_method, destruction_method.__name__, len(D_initial), len(D_final)))
        
        nx.draw(G, pos, with_labels=True, font_weight='bold', ax=axes[i, 0])
        axes[i, 0].set_title(f'Grafo Original ({init_method} + {destruction_method.__name__})')

        nx.draw_networkx_nodes(G, pos, nodelist=D_initial, node_color='red', node_size=200, ax=axes[i, 1])
        nx.draw_networkx_edges(G, pos, ax=axes[i, 1])
        axes[i, 1].set_title('Solução Inicial')

        nx.draw_networkx_nodes(G, pos, nodelist=D_final, node_color='green', node_size=200, ax=axes[i, 2])
        nx.draw_networkx_edges(G, pos, ax=axes[i, 2])
        axes[i, 2].set_title('Solução Final')

    plt.tight_layout()
    plt.savefig("resultado.png")

    df_results = pd.DataFrame(results, columns=['Método Inicial', 'Método de Destruição', 'Tamanho Inicial', 'Tamanho Final'])
    print(df_results)
