'''
Implementação do algoritmo Minimax para o jogo Tapatan.
'''

class MinimaxAlgoritmo:
    """
    Implementação do algoritmo Minimax com poda alfa-beta.
    """
    
    @staticmethod
    def jogador(estado):
        """
        Retorna qual jogador ('X' ou 'O') deve jogar no estado atual.
        
        Args:
            estado (Estado): O estado atual do jogo
            
        Returns:
            str: 'X' ou 'O' representando o jogador atual
        """
        return estado.jogador_atual
    
    @staticmethod
    def acoes(estado):
        """
        Retorna todas as jogadas disponíveis no estado atual.
        
        Args:
            estado (Estado): O estado atual do jogo
            
        Returns:
            list: Lista de tuplas (origem, destino) representando os movimentos disponíveis
        """
        jogadas = []
        simbolo = MinimaxAlgoritmo.jogador(estado)
        
        # Encontrar todas as peças do jogador atual
        pecas = []
        for i in range(3):
            for j in range(3):
                if estado.tabuleiro[i][j] == simbolo:
                    pecas.append((i, j))
        
        # Para cada peça, encontrar todos os movimentos possíveis
        for origem in pecas:
            for destino in estado.conexoes[origem]:
                # Verificar se o destino está vazio
                if destino[0] < 0 or destino[0] > 2 or destino[1] < 0 or destino[1] > 2:
                    continue
                if estado.tabuleiro[destino[0]][destino[1]] == ' ':
                    jogadas.append((origem, destino))
        
        return jogadas
    
    @staticmethod
    def resultado(estado, acao):
        """
        Retorna o novo estado após aplicar uma ação ao estado atual.
        
        Args:
            estado (Estado): O estado atual do jogo
            acao (tuple): Tupla (origem, destino) representando o movimento
            
        Returns:
            Estado: Novo estado após aplicar a ação
        """
        from estado import Estado
        
        # Criar uma cópia do estado para não modificar o original
        novo_estado = Estado(estado.tabuleiro, estado.jogador_atual)
        
        origem, destino = acao
        
        # Aplicar o movimento
        simbolo = novo_estado.tabuleiro[origem[0]][origem[1]]
        novo_estado.tabuleiro[origem[0]][origem[1]] = ' '
        novo_estado.tabuleiro[destino[0]][destino[1]] = simbolo
        
        # Trocar o jogador
        novo_estado.jogador_atual = 'O' if novo_estado.jogador_atual == 'X' else 'X'
        
        return novo_estado
    
    @staticmethod
    def ganhador(estado):
        """
        Retorna o símbolo do jogador que ganhou, se houver.
        
        Args:
            estado (Estado): O estado atual do jogo
            
        Returns:
            str ou None: 'X', 'O' ou None se não houver ganhador
        """
        # Verificar linhas
        for i in range(3):
            if estado.tabuleiro[i][0] == estado.tabuleiro[i][1] == estado.tabuleiro[i][2] != ' ':
                return estado.tabuleiro[i][0]
        
        # Verificar colunas
        for j in range(3):
            if estado.tabuleiro[0][j] == estado.tabuleiro[1][j] == estado.tabuleiro[2][j] != ' ':
                return estado.tabuleiro[0][j]
        
        # Verificar diagonais
        if estado.tabuleiro[0][0] == estado.tabuleiro[1][1] == estado.tabuleiro[2][2] != ' ':
            return estado.tabuleiro[0][0]
        
        if estado.tabuleiro[0][2] == estado.tabuleiro[1][1] == estado.tabuleiro[2][0] != ' ':
            return estado.tabuleiro[0][2]
        
        return None
    
    @staticmethod
    def final(estado):
        """
        Retorna True se o jogo acabou, False caso contrário.
        
        Args:
            estado (Estado): O estado atual do jogo
            
        Returns:
            bool: True se o jogo acabou, False caso contrário
        """
        # O jogo acaba se houver um ganhador
        if MinimaxAlgoritmo.ganhador(estado) is not None:
            return True
        
        # O jogo também acaba se não houver mais movimentos possíveis
        return len(MinimaxAlgoritmo.acoes(estado)) == 0
    
    @staticmethod
    def custo(estado):
        """
        Retorna 1 se X ganhou, -1 se O ganhou, 0 caso contrário.
        
        Args:
            estado (Estado): O estado atual do jogo
            
        Returns:
            int: 1 se X ganhou, -1 se O ganhou, 0 caso contrário
        """
        vencedor = MinimaxAlgoritmo.ganhador(estado)
        
        if vencedor == 'X':
            return 1
        elif vencedor == 'O':
            return -1
        else:
            return 0
    
    @staticmethod
    def minimax(estado, profundidade=3, alfa=float('-inf'), beta=float('inf'), maximizando=True):
        """
        Implementa o algoritmo minimax com poda alfa-beta para determinar o melhor movimento.
        
        Args:
            estado (Estado): O estado atual do jogo
            profundidade (int): A profundidade máxima da busca
            alfa (float): O valor alfa para poda alfa-beta
            beta (float): O valor beta para poda alfa-beta
            maximizando (bool): True se estamos maximizando, False se estamos minimizando
            
        Returns:
            tuple: (melhor_valor, melhor_acao) - o melhor valor e a melhor ação encontrados
        """
        # Caso base: jogo acabou ou atingiu profundidade máxima
        if profundidade == 0 or MinimaxAlgoritmo.final(estado):
            return MinimaxAlgoritmo.custo(estado), None
        
        # Inicializar melhor ação e valor
        melhor_acao = None
        
        if maximizando:
            melhor_valor = float('-inf')
            # Para cada ação possível
            for acao in MinimaxAlgoritmo.acoes(estado):
                # Calcular o valor minimax do resultado dessa ação
                novo_estado = MinimaxAlgoritmo.resultado(estado, acao)
                valor, _ = MinimaxAlgoritmo.minimax(novo_estado, profundidade - 1, alfa, beta, False)
                
                # Atualizar melhor valor e ação, se necessário
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_acao = acao
                
                # Atualizar alfa
                alfa = max(alfa, melhor_valor)
                
                # Poda alfa-beta
                if beta <= alfa:
                    break
                
            return melhor_valor, melhor_acao
        else:
            melhor_valor = float('inf')
            # Para cada ação possível
            for acao in MinimaxAlgoritmo.acoes(estado):
                # Calcular o valor minimax do resultado dessa ação
                novo_estado = MinimaxAlgoritmo.resultado(estado, acao)
                valor, _ = MinimaxAlgoritmo.minimax(novo_estado, profundidade - 1, alfa, beta, True)
                
                # Atualizar melhor valor e ação, se necessário
                if valor < melhor_valor:
                    melhor_valor = valor
                    melhor_acao = acao
                
                # Atualizar beta
                beta = min(beta, melhor_valor)
                
                # Poda alfa-beta
                if beta <= alfa:
                    break
                
            return melhor_valor, melhor_acao