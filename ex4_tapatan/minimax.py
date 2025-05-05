'''
Implementação do algoritmo Minimax para o jogo Tapatan.

-> Versão otimizada para criar uma IA praticamente imbatível.
'''

class MinimaxAlgoritmo:
    """
    Implementação do algoritmo Minimax com poda alfa-beta e otimizações para IA imbatível.
    """
    
    @staticmethod
    def jogador(estado):
        """
        Retorna qual jogador ('X' ou 'O') deve jogar no estado atual.
        """
        return estado.jogador_atual
    
    @staticmethod
    def acoes(estado):
        """
        Retorna todas as jogadas disponíveis no estado atual.
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
        """
        # O jogo acaba se houver um ganhador
        if MinimaxAlgoritmo.ganhador(estado) is not None:
            return True
        
        # O jogo também acaba se não houver mais movimentos possíveis
        return len(MinimaxAlgoritmo.acoes(estado)) == 0
    
    @staticmethod
    def avaliar_posicao(estado, simbolo_computador):
        """
        Função avançada de avaliação para favorecer o computador.
        Retorna um valor heurístico para estados não terminais.
        
        Args:
            estado: O estado atual do jogo
            simbolo_computador: O símbolo do computador ('X' ou 'O')
            
        Returns:
            float: Valor heurístico da posição atual
        """
        # Verificar se há um vencedor
        vencedor = MinimaxAlgoritmo.ganhador(estado)
        if vencedor == simbolo_computador:
            return 100  # Computador venceu
        elif vencedor is not None:
            return -100  # Jogador humano venceu
        
        simbolo_humano = 'O' if simbolo_computador == 'X' else 'X'
        valor = 0
        
        # Favorecimento do centro - posição estratégica
        if estado.tabuleiro[1][1] == simbolo_computador:
            valor += 3
        elif estado.tabuleiro[1][1] == simbolo_humano:
            valor -= 3
        
        # Avaliar possibilidades de 2-em-linha
        # Para o computador
        valor += MinimaxAlgoritmo._contar_dois_em_linha(estado, simbolo_computador) * 5
        # Para o humano
        valor -= MinimaxAlgoritmo._contar_dois_em_linha(estado, simbolo_humano) * 5
        
        # Avaliar mobilidade (número de movimentos possíveis)
        # Original do jogador atual
        jogador_atual = estado.jogador_atual
        
        # Temporariamente mudar para computador e calcular mobilidade
        estado.jogador_atual = simbolo_computador
        movimentos_computador = len(MinimaxAlgoritmo.acoes(estado))
        valor += movimentos_computador * 0.5
        
        # Temporariamente mudar para humano e calcular mobilidade
        estado.jogador_atual = simbolo_humano
        movimentos_humano = len(MinimaxAlgoritmo.acoes(estado))
        valor -= movimentos_humano * 0.5
        
        # Restaurar jogador original
        estado.jogador_atual = jogador_atual
        
        # Favorecimento de posições próximas de peças próprias
        valor += MinimaxAlgoritmo._avaliar_proximidade(estado, simbolo_computador)
        
        return valor
    
    @staticmethod
    def _contar_dois_em_linha(estado, simbolo):
        """
        Conta quantas configurações de 2-em-linha o jogador tem.
        Isso indica posições quase vencedoras.
        """
        contador = 0
        
        # Verificar linhas
        for i in range(3):
            if (estado.tabuleiro[i][0] == estado.tabuleiro[i][1] == simbolo and estado.tabuleiro[i][2] == ' ') or \
               (estado.tabuleiro[i][0] == estado.tabuleiro[i][2] == simbolo and estado.tabuleiro[i][1] == ' ') or \
               (estado.tabuleiro[i][1] == estado.tabuleiro[i][2] == simbolo and estado.tabuleiro[i][0] == ' '):
                contador += 1
        
        # Verificar colunas
        for j in range(3):
            if (estado.tabuleiro[0][j] == estado.tabuleiro[1][j] == simbolo and estado.tabuleiro[2][j] == ' ') or \
               (estado.tabuleiro[0][j] == estado.tabuleiro[2][j] == simbolo and estado.tabuleiro[1][j] == ' ') or \
               (estado.tabuleiro[1][j] == estado.tabuleiro[2][j] == simbolo and estado.tabuleiro[0][j] == ' '):
                contador += 1
        
        # Verificar diagonais
        if (estado.tabuleiro[0][0] == estado.tabuleiro[1][1] == simbolo and estado.tabuleiro[2][2] == ' ') or \
           (estado.tabuleiro[0][0] == estado.tabuleiro[2][2] == simbolo and estado.tabuleiro[1][1] == ' ') or \
           (estado.tabuleiro[1][1] == estado.tabuleiro[2][2] == simbolo and estado.tabuleiro[0][0] == ' '):
            contador += 1
        
        if (estado.tabuleiro[0][2] == estado.tabuleiro[1][1] == simbolo and estado.tabuleiro[2][0] == ' ') or \
           (estado.tabuleiro[0][2] == estado.tabuleiro[2][0] == simbolo and estado.tabuleiro[1][1] == ' ') or \
           (estado.tabuleiro[1][1] == estado.tabuleiro[2][0] == simbolo and estado.tabuleiro[0][2] == ' '):
            contador += 1
        
        return contador
    
    @staticmethod
    def _avaliar_proximidade(estado, simbolo):
        """
        Avalia quão próximas estão as peças do jogador entre si.
        Proximidade entre peças pode levar a melhores chances de formar linha.
        """
        valor = 0
        pecas = []
        
        # Encontrar todas as peças do jogador
        for i in range(3):
            for j in range(3):
                if estado.tabuleiro[i][j] == simbolo:
                    pecas.append((i, j))
        
        # Calcular proximidade entre peças (menor distância = melhor)
        for i, peca1 in enumerate(pecas):
            for peca2 in pecas[i+1:]:
                distancia = abs(peca1[0] - peca2[0]) + abs(peca1[1] - peca2[1])
                if distancia <= 1:  # Peças adjacentes
                    valor += 2
                elif distancia == 2:  # Peças a uma casa de distância
                    valor += 1
        
        return valor
    
    @staticmethod
    def custo(estado, simbolo_computador='O'):
        """
        Retorna 1 se X ganhou, -1 se O ganhou, 0 caso contrário.
        Modificado para incluir avaliação heurística para estados não terminais.
        """
        vencedor = MinimaxAlgoritmo.ganhador(estado)
        
        if vencedor == 'X':
            return 1
        elif vencedor == 'O':
            return -1
        elif MinimaxAlgoritmo.final(estado):
            return 0
        else:
            # Para estados não terminais, usar a função de avaliação
            return MinimaxAlgoritmo.avaliar_posicao(estado, simbolo_computador) / 100
    
    @staticmethod
    def minimax(estado, profundidade=5, alfa=float('-inf'), beta=float('inf'), maximizando=True, simbolo_computador='O'):
        """
        Implementa o algoritmo minimax com poda alfa-beta para determinar o melhor movimento.
        Profundidade maior (5) e avaliação de posição melhorada.
        """
        # Caso base: jogo acabou ou atingiu profundidade máxima
        if profundidade == 0 or MinimaxAlgoritmo.final(estado):
            return MinimaxAlgoritmo.custo(estado, simbolo_computador), None
        
        # Inicializar melhor ação e valor
        melhor_acao = None
        
        if maximizando:
            melhor_valor = float('-inf')
            # Para cada ação possível
            for acao in MinimaxAlgoritmo.acoes(estado):
                # Calcular o valor minimax do resultado dessa ação
                novo_estado = MinimaxAlgoritmo.resultado(estado, acao)
                valor, _ = MinimaxAlgoritmo.minimax(novo_estado, profundidade - 1, alfa, beta, False, simbolo_computador)
                
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
                valor, _ = MinimaxAlgoritmo.minimax(novo_estado, profundidade - 1, alfa, beta, True, simbolo_computador)
                
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