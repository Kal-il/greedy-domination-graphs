import networkx as nx
import matplotlib.pyplot as plt

def check_dominante(dominante, G):
    dominados = set(dominante)
    for v in dominante:
        dominados.update(G.neighbors(v))
    return dominados == set(G.nodes)

# Greedy Insertion Procedure
def insercao_inicial_gulosa(G):
    v_folhas = {v for v in G.nodes if len(list(G.neighbors(v))) == 1}
    v_suporte = {u for v in v_folhas for u in G.neighbors(v)}

    dominante = v_suporte.copy()

    # Função gulosa gGIP(v): calcula a contribuição de um vértice v
    def gGIP(v, dominant):
        # Contribuição é o número de vértices adjacentes a v que não são dominados por D
        N_v = set(G.neighbors(v)) | {v}
        N_dominantes = set(neighbor for u in dominant for neighbor in G.neighbors(u)) | dominant
        return len(N_v - N_dominantes)

    # Seleciona vértices iterativamente até que D se torne um conjunto dominante
    while not check_dominante(dominante, G):
        # Seleciona o vértice com a maior contribuição gulosa que não está em D nem em L
        candidates = (v for v in G.nodes if v not in dominante and v not in v_folhas)
        v_best = max(candidates, key=lambda v: gGIP(v, dominante))
        dominante.add(v_best)
    print(dominante)

    return dominante


def InitialSolution(G):
    pass

def LocalImprovement(D):
    pass

def Destruction(D, beta):
    pass

def Reconstruction(D):
    pass


# Algoritimo base do Iterated greddy descrito no pseudocódigo
"""
    - G -> um grafo de entrada
    - beta -> a porcentagem de vértices removidos na fase de destruição
    - delta_max -> Número máximo de iterações sem melhoria que IG permite realizar.
"""
# def IG(G, beta, delta_max):
#     dominante = insercao_inicial_gulosa(G)
#     D_b = LocalImprovement(dominante)
#     delta = 0;
#
#     while delta < delta_max:
#         D_d = Destruction(D_b, beta)
#         D_r = Reconstruction(D_d)
#         D_i = LocalImprovement(D_r)
#
#         if len(D_i) < len(D_b):3
#             D_b = D_i
#             delta = 0
#         else:
#             delta += 1
#     return D_b







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    G = nx.Graph()

    # Adicionando arestas para formar folhas e suportes
    edges = [
        (1, 2), (1, 3),  # Vértices de suporte: 1
        (4, 1),  # Vértice folha: 4
        (5, 1),  # Vértice folha: 5
        (6, 7),  # Vértices de suporte: 6
        (8, 6),  # Vértice folha: 8
        (9, 7),  # Vértice folha: 9
        (10, 7),  # Vértice folha: 10
        (3, 11), (3, 12),  # Outros vértices conectados a 3
        (7, 13)  # Conexão extra
    ]

    # Adiciona as arestas ao grafo
    G.add_edges_from(edges)

    nx.draw(G, with_labels=True)
    plt.show()

    # Testando a função de solução inicial
    D_initial = insercao_inicial_gulosa(G)
    print("Conjunto dominante inicial:", D_initial)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/