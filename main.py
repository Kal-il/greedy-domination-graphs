# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


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
def IG(G, beta, delta_max):
    D = InitialSolution(G)
    D_b = LocalImprovement(D)
    delta = 0;

    while delta < delta_max:
        D_d = Destruction(D_b, beta)
        D_r = Reconstruction(D_d)
        D_i = LocalImprovement(D_r)

        if D_i < D_b:
            D_b = D_i
            delta = 0
        else:
            delta += 1
    return D_b







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
