import networkx as nx
from collections import defaultdict

def calcular_mis(aristas_grafo):
    """Calcula el MIS para grafos outerplanares (árboles y ciclos)"""
    if not aristas_grafo.strip():
        return 0  # Grafo vacío
    
    try:
        # Procesamiento robusto de aristas
        aristas = []
        for parte in aristas_grafo.split(','):
            parte = parte.strip()
            if not parte:
                continue
            u, v = map(str.strip, parte.split('-'))
            aristas.append((u, v))
        G = nx.Graph(aristas)
    except Exception as e:
        return f"Error en formato: {str(e)}. Ejemplo válido: '1-2,2-3,3-1'"

    # Algoritmo para árboles (DP approach)
    def mis_arbol(grafo):
        if not grafo.nodes():
            return 0
            
        root = next(iter(grafo.nodes()))
        dp = defaultdict(dict)
        
        def dfs(node, parent):
            incl = 1  # Incluyendo el nodo actual
            excl = 0   # Excluyendo el nodo actual
            
            for neighbor in grafo.neighbors(node):
                if neighbor != parent:
                    dfs(neighbor, node)
                    incl += dp[neighbor]['excl']
                    excl += max(dp[neighbor]['incl'], dp[neighbor]['excl'])
            
            dp[node]['incl'] = incl
            dp[node]['excl'] = excl
        
        dfs(root, None)
        return max(dp[root]['incl'], dp[root]['excl'])

    # Algoritmo para ciclos outerplanares
    def mis_ciclo(grafo):
        try:
            ciclos = nx.cycle_basis(grafo)
            if not ciclos:
                return mis_arbol(grafo)  # Si no hay ciclos, es un árbol
                
            ciclo = ciclos[0]  # Tomamos el primer ciclo
            return len(ciclo) // 2  # Fórmula general para ciclos
        except:
            return mis_arbol(grafo)  # Fallback a algoritmo de árboles

    # Determinar qué algoritmo usar
    if nx.is_tree(G):
        return mis_arbol(G)
    else:
        return mis_ciclo(G)

# Interfaz de usuario
if __name__ == "__main__":
    print("\nCalculador de MIS para grafos outerplanares (árboles y ciclos)")
    print("Ingrese aristas como se muestra en el siguiente ejemplo:'1-2,2-3' o 'Salir' para terminar.\n")
    
    while True:
        entrada = input("Aristas: ").strip()
        if entrada.lower() == 'salir':
            break
            
        resultado = calcular_mis(entrada)
        print(f" Tamaño del MIS: {resultado}\n")