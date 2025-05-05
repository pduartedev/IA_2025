'''
Estado do jogo Tapatan.
Encapsula o tabuleiro e o jogador atual.
'''

import copy

class Estado:
    """
    Classe para representar um estado do jogo.
    Encapsula o tabuleiro e o jogador atual.
    """
    def __init__(self, tabuleiro=None, jogador_atual='X'):
        # Inicializa o tabuleiro padrão se nenhum for fornecido
        if tabuleiro is None:
            self.tabuleiro = [
                ['X', 'O', 'X'], 
                [' ', ' ', ' '], 
                ['O', 'X', 'O']
            ]
        else:
            # Cria uma cópia profunda do tabuleiro para evitar referências
            self.tabuleiro = copy.deepcopy(tabuleiro)
        
        self.jogador_atual = jogador_atual
        
        # Define as conexões válidas no tabuleiro (movimentos possíveis)
        self.conexoes = {
            (0, 0): [(0, 1), (1, 0), (1, 1)],
            (0, 1): [(0, 0), (0, 2), (1, 1)],
            (0, 2): [(0, 1), (1, 1), (1, 2)],
            (1, 0): [(0, 0), (1, 1), (2, 0)],
            (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
            (1, 2): [(0, 2), (1, 1), (2, 2)],
            (2, 0): [(1, 0), (1, 1), (2, 1)],
            (2, 1): [(2, 0), (1, 1), (2, 2)],
            (2, 2): [(2, 1), (1, 1), (1, 2)]
        }