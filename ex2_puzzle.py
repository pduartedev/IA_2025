import heapq
import numpy as np
from copy import deepcopy
import time

class Puzzle:
    """
    Inicializa um nó do quebra-cabeça.
        
    Args:
        estado: Matriz 3x3 representando as posições das peças
        pai: Nó pai de onde este nó foi gerado
        acao: Ação tomada para chegar a este estado ("Cima", "Baixo", "Esquerda", "Direita")
        custo: Custo g(n) - número de movimentos desde o início
    """
    
    def __init__(self, estado, pai=None, acao=None, custo=0):    
        self.estado = estado  # Configuração atual do tabuleiro
        self.pai = pai  # Nó pai, para reconstruir o caminho da solução
        self.acao = acao  # Movimento que gerou este estado
        self.custo = custo  # g(n): custo do caminho até aqui
        self.heuristica = self.calcular_manhattan()  # h(n): estimativa até o objetivo TODO: VERIFICAR
        self.f = self.custo + self.heuristica  # f(n) = g(n) + h(n) para A*

    """
    Define como comparar dois nós (usado pela fila de prioridade).
    Nós são ordenados pelo valor de f = g + h.
    """
    def __lt__(self, outro):
        return self.f < outro.f
    
    """
    Encontra a posição (linha, coluna) de um valor específico no tabuleiro.
    
    Args:
        valor: O valor a ser localizado (0 para o espaço vazio)
    
    Returns:
        Tupla (linha, coluna) com a posição
    """
    def encontrar_posicao(self, valor):
        for i in range(3):
            for j in range(3):
                if self.estado[i][j] == valor:
                    return i, j
        return -1, -1  # Valor não encontrado (não deveria acontecer)
    

    """
    Calcula a heurística da distância de Manhattan para este estado.
    Soma as distâncias de cada peça até sua posição objetivo.
    
    Returns:
        Soma total das distâncias de Manhattan
    """
    def calcular_manhattan(self):
        distancia = 0
        for i in range(3):
            for j in range(3):
                valor = self.estado[i][j]
                if valor != 0:  # Ignora o espaço vazio
                    # Calcula onde o valor deveria estar no estado objetivo
                    linha_objetivo = (valor - 1) // 3
                    coluna_objetivo = (valor - 1) % 3
                    # Soma a distância Manhattan (|x1 - x2| + |y1 - y2|)
                    distancia += abs(i - linha_objetivo) + abs(j - coluna_objetivo)
        return distancia
    
        """
        Gera todos os estados sucessores possíveis movendo o espaço vazio.
        
        Returns:
            Lista de nós Puzzle que podem ser alcançados com um movimento
        """
    def gerar_sucessores(self):
        i, j = self.encontrar_posicao(0)  # Encontra o espaço vazio (0)
        sucessores = []
        
        # Define os quatro movimentos possíveis (nome, delta_linha, delta_coluna)
        movimentos = [
            ('Cima', -1, 0),      # Mover o espaço vazio para cima
            ('Baixo', 1, 0),      # Mover o espaço vazio para baixo
            ('Esquerda', 0, -1),  # Mover o espaço vazio para a esquerda
            ('Direita', 0, 1)     # Mover o espaço vazio para a direita
        ]
        
        for acao, di, dj in movimentos:
            nova_i, nova_j = i + di, j + dj
            
            # Verifica se o movimento é válido (dentro dos limites do tabuleiro)
            if 0 <= nova_i < 3 and 0 <= nova_j < 3:
                # Cria uma cópia profunda do estado atual
                novo_estado = deepcopy(self.estado)
                # Troca a posição do espaço vazio com a peça adjacente
                novo_estado[i][j], novo_estado[nova_i][nova_j] = novo_estado[nova_i][nova_j], novo_estado[i][j]
                
                # Cria um novo nó com o estado resultante, incrementando o custo
                sucessor = Puzzle(novo_estado, self, acao, self.custo + 1)
                sucessores.append(sucessor)
                
        return sucessores
    
    """
    Verifica se este estado é o objetivo.
    
    Args:
        estado_objetivo: Estado objetivo para comparação
    
    Returns:
        True se este estado for igual ao objetivo, False caso contrário
    """
    def eh_objetivo(self, estado_objetivo):
        return self.estado == estado_objetivo
    
    """
    Define a igualdade entre dois nós (baseada apenas no estado).
    """
    def __eq__(self, outro):
        return self.estado == outro.estado
    
    def __hash__(self):
        """
        Função hash para permitir que estados sejam usados em conjuntos e dicionários.
        """
        return hash(str(self.estado))

    """
    Implementa o algoritmo A* para encontrar o caminho ótimo.

    Args:
        estado_inicial: Matriz 3x3 representando o estado inicial
        estado_objetivo: Matriz 3x3 representando o estado objetivo

    Returns:
        Tupla (caminho, nos_expandidos, tempo) com a solução encontrada,
        ou (None, nos_expandidos, tempo) se não houver solução
    """
def busca_a_estrela(estado_inicial, estado_objetivo):
    # Inicialização das estruturas de dados
    fronteira = []  # Fila de prioridade (heap) para a fronteira
    no_inicial = Puzzle(estado_inicial)  # Cria o nó inicial
    heapq.heappush(fronteira, no_inicial)  # Adiciona o nó inicial à fronteira
    explorados = set()  # Conjunto de estados já explorados
    estados_fronteira = {str(estado_inicial)}  # Estados atualmente na fronteira
    
    # Métricas para análise do algoritmo
    nos_expandidos = 0
    
    inicio = time.time()  # Marca o tempo de início
    
    # Loop principal da busca - implementa o pseudocódigo fornecido
    while fronteira:
        # Se a fronteira estiver vazia, não há solução
        if not fronteira:
            return None, nos_expandidos, time.time() - inicio
        
        # Remove o nó com menor f(n) da fronteira (passo 1 do pseudocódigo)
        no_atual = heapq.heappop(fronteira)
        estados_fronteira.remove(str(no_atual.estado))
        
        # Verifica se chegou ao objetivo (passo 2 do pseudocódigo)
        if no_atual.eh_objetivo(estado_objetivo):
            fim = time.time()
            tempo = fim - inicio
            
            # Reconstrói o caminho da solução seguindo os nós pais
            caminho = []
            while no_atual.pai:
                caminho.append((no_atual.acao, no_atual.estado))
                no_atual = no_atual.pai
            caminho.reverse()  # Inverte para obter do início ao fim
            
            return caminho, nos_expandidos, tempo
        
        # Adiciona o nó atual ao conjunto de explorados (último passo do pseudocódigo)
        explorados.add(str(no_atual.estado))
        nos_expandidos += 1
        
        # Expande o nó atual e adiciona sucessores à fronteira (passo 3 do pseudocódigo)
        for sucessor in no_atual.gerar_sucessores():
            estado_str = str(sucessor.estado)
            
            # Verifica se o estado não foi explorado e não está na fronteira
            if estado_str not in explorados and estado_str not in estados_fronteira:
                heapq.heappush(fronteira, sucessor)
                estados_fronteira.add(estado_str)
    
    # Se saiu do loop sem encontrar solução, não há solução
    return None, nos_expandidos, time.time() - inicio

def imprimir_estado(estado):
    """
    Imprime o estado do tabuleiro de forma legível.
    
    Args:
        estado: Matriz 3x3 representando um estado do tabuleiro
    """
    for linha in estado:
        print(linha)
    print()

# Exemplo de uso
def main():
    """
    Função principal que define os estados e executa o algoritmo.
    """
    # Estado inicial (pode ser alterado para testar diferentes configurações)
    estado_inicial = [
        [7, 2, 4],
        [5, 0, 6],  # 0 representa o espaço vazio
        [8, 3, 1]
    ]
    
    # Estado objetivo - configuração ordenada
    estado_objetivo = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]  # 0 na posição final inferior direita
    ]
    
    print("Estado Inicial:")
    imprimir_estado(estado_inicial)
    
    print("Estado Objetivo:")
    imprimir_estado(estado_objetivo)
    
    print("Resolvendo...")
    solucao, nos_expandidos, tempo = busca_a_estrela(estado_inicial, estado_objetivo)
    
    # Exibe os resultados
    if solucao:
        print(f"Solução encontrada em {len(solucao)} movimentos!")
        print(f"Nós expandidos: {nos_expandidos}")
        print(f"Tempo de execução: {tempo:.4f} segundos")
        
        print("\nSequência de movimentos:")
        estado_atual = estado_inicial
        imprimir_estado(estado_atual)
        
        # Mostra cada passo da solução
        for acao, estado in solucao:
            print(f"Movimento: {acao}")
            imprimir_estado(estado)
    else:
        print("Não foi possível encontrar uma solução.")

if __name__ == "__main__":
    main()