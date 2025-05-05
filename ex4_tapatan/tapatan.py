'''
Jogo Tapatan - Uma variação do jogo da velha onde cada jogador começa
com 3 peças já no tabuleiro e deve movê-las para formar uma linha.
Implementação usando o algoritmo Minimax para a IA do computador.
'''

import os
import time
from estado import Estado
from minimax import MinimaxAlgoritmo

class Tapatan:
    def __init__(self):
        # Estado inicial do jogo
        self.estado = Estado()
        
        # Flag para indicar se é modo de jogo contra o computador
        self.modo_computador = False
        
        # Símbolo do jogador humano (padrão: X)
        self.simbolo_humano = 'X'
        # Símbolo do computador (padrão: O)
        self.simbolo_computador = 'O'
        
        # Contador para acompanhar o número de turnos
        self.turnos = 0
        
        # Profundidade fixa para o minimax (IA imbatível)
        self.dificuldade = 5
    
    def limpar_tela(self):
        """Limpa a tela do console"""
        # Para Windows
        if os.name == 'nt':
            os.system('cls')
        # Para Mac e Linux
        else:
            os.system('clear')
    
    def exibir_tabuleiro(self):
        """Exibe o tabuleiro atual na tela em formato melhorado"""
        print("\n  TAPATAN\n")
        
        if self.modo_computador:
            if self.estado.jogador_atual == self.simbolo_humano:
                print(f"Sua vez (Jogador {self.simbolo_humano})")
            else:
                print(f"Vez do computador (Jogador {self.simbolo_computador})")
        else:
            print(f"Jogador atual: {self.estado.jogador_atual}")
        
        print("")  # Linha em branco
        
        # Exibe índices das colunas
        print("     0     1     2  ")
        print("  ┌─────┬─────┬─────┐")
        
        # Exibe o tabuleiro com linhas numeradas e formatação melhorada
        for i, linha in enumerate(self.estado.tabuleiro):
            print(f"{i} │  {linha[0]}  │  {linha[1]}  │  {linha[2]}  │")
            if i < 2:
                print("  ├─────┼─────┼─────┤")
            else:
                print("  └─────┴─────┴─────┘")
    
    def encontrar_pecas(self, simbolo):
        """
        Encontra todas as posições das peças de um jogador específico
        
        Args:
            simbolo (str): 'X' ou 'O' representando o jogador
            
        Returns:
            list: Lista de tuplas (linha, coluna) com as posições das peças
        """
        pecas = []
        for i in range(3):
            for j in range(3):
                if self.estado.tabuleiro[i][j] == simbolo:
                    pecas.append((i, j))
        return pecas
    
    def verificar_movimento_valido(self, origem, destino):
        """
        Verifica se um movimento é válido
        
        Args:
            origem (tuple): Coordenadas (linha, coluna) da peça a ser movida
            destino (tuple): Coordenadas (linha, coluna) do destino
            
        Returns:
            bool: True se o movimento é válido, False caso contrário
        """
        # Verifica se o destino está vazio
        if self.estado.tabuleiro[destino[0]][destino[1]] != ' ':
            return False
        
        # Verifica se o destino é uma conexão válida da origem
        if destino not in self.estado.conexoes[origem]:
            return False
        
        return True
    
    def mover_peca(self, origem, destino):
        """
        Move uma peça no tabuleiro
        
        Args:
            origem (tuple): Coordenadas (linha, coluna) da peça a ser movida
            destino (tuple): Coordenadas (linha, coluna) do destino
        """
        simbolo = self.estado.tabuleiro[origem[0]][origem[1]]
        self.estado.tabuleiro[origem[0]][origem[1]] = ' '
        self.estado.tabuleiro[destino[0]][destino[1]] = simbolo
        
        # Trocar o jogador atual
        self.estado.jogador_atual = 'O' if self.estado.jogador_atual == 'X' else 'X'
    
    def mostrar_movimentos_possiveis(self, origem):
        """
        Mostra os movimentos possíveis para uma determinada peça
        
        Args:
            origem (tuple): Coordenadas (linha, coluna) da peça
            
        Returns:
            list: Lista de tuplas (linha, coluna) com os movimentos possíveis
        """
        movimentos = []
        for destino in self.estado.conexoes[origem]:
            if self.estado.tabuleiro[destino[0]][destino[1]] == ' ':
                movimentos.append(destino)
        return movimentos
    
    def movimento_computador(self):
        """
        Determina o movimento do computador usando o algoritmo Minimax.
        
        Returns:
            tuple: Tupla contendo as coordenadas de origem e destino do movimento
        """
        # Ajustar o maximizando com base no símbolo do computador
        maximizando = self.simbolo_computador == 'X'
        
        print("\nAnalisando possíveis movimentos...")
        
        # Chamar o algoritmo minimax com profundidade fixa e avaliação melhorada
        _, melhor_acao = MinimaxAlgoritmo.minimax(
            self.estado, 
            profundidade=self.dificuldade, 
            maximizando=maximizando, 
            simbolo_computador=self.simbolo_computador
        )
        
        return melhor_acao
    
    def jogar(self):
        """Função principal para executar o jogo"""
        while True:
            self.limpar_tela()
            self.exibir_tabuleiro()
            
            # Verificar se há um vencedor
            vencedor = MinimaxAlgoritmo.ganhador(self.estado)
            if vencedor:
                if self.modo_computador:
                    if vencedor == self.simbolo_humano:
                        print(f"\nParabéns! Você venceu!")
                    else:
                        print(f"\nO computador venceu!")
                else:
                    print(f"\nJogador {vencedor} venceu!")
                break
            
            # Verificar se o jogo acabou sem vencedor
            if MinimaxAlgoritmo.final(self.estado) and not vencedor:
                print("\nJogo terminou empatado!")
                break
            
            # Turno do computador
            if self.modo_computador and self.estado.jogador_atual == self.simbolo_computador:
                print("\nO computador está pensando...")
                time.sleep(1)  # Pequena pausa para simular "pensamento"
                
                movimento = self.movimento_computador()
                if movimento:
                    origem, destino = movimento
                    print(f"O computador moveu a peça da posição ({origem[0]}, {origem[1]}) para ({destino[0]}, {destino[1]})")
                    self.mover_peca(origem, destino)
                    time.sleep(1.5)  # Pausa para o jogador ver o movimento
                    self.turnos += 1
                    continue
                else:
                    print("Erro no movimento do computador. Tente novamente.")
                    time.sleep(1.5)
                    continue
            
            # Turno do jogador humano
            # Encontrar as peças do jogador atual
            pecas_jogador = self.encontrar_pecas(self.estado.jogador_atual)
            
            # Mostrar as peças disponíveis para movimento
            print(f"\nPeças do jogador {self.estado.jogador_atual}:")
            for i, peca in enumerate(pecas_jogador):
                print(f"{i+1}. Posição ({peca[0]}, {peca[1]})")
            
            try:
                # Selecionar uma peça para mover
                escolha = int(input("\nEscolha uma peça para mover (1-3): ")) - 1
                if escolha < 0 or escolha >= len(pecas_jogador):
                    print("Escolha inválida! Tente novamente.")
                    time.sleep(1.5)
                    continue
                
                origem = pecas_jogador[escolha]
                
                # Mostrar movimentos possíveis
                movimentos_possiveis = self.mostrar_movimentos_possiveis(origem)
                if not movimentos_possiveis:
                    print("Não há movimentos válidos para esta peça. Escolha outra.")
                    time.sleep(1.5)
                    continue
                
                print(f"\nMovimentos possíveis para a peça na posição ({origem[0]}, {origem[1]}):")
                for i, movimento in enumerate(movimentos_possiveis):
                    print(f"{i+1}. Mover para ({movimento[0]}, {movimento[1]})")
                
                # Selecionar um destino
                movimento_escolhido = int(input("\nEscolha um movimento (1-" + str(len(movimentos_possiveis)) + "): ")) - 1
                if movimento_escolhido < 0 or movimento_escolhido >= len(movimentos_possiveis):
                    print("Movimento inválido! Tente novamente.")
                    time.sleep(1.5)
                    continue
                
                destino = movimentos_possiveis[movimento_escolhido]
                
                # Realizar o movimento
                self.mover_peca(origem, destino)
                
                # Incrementar o contador de turnos
                self.turnos += 1
                
            except ValueError:
                print("Entrada inválida! Por favor, digite um número.")
                time.sleep(1.5)
            except Exception as e:
                print(f"Erro: {e}")
                time.sleep(1.5)

    def configurar_modo_jogo(self):
        """Configura o modo de jogo (contra computador ou contra outro jogador)"""
        self.limpar_tela()
        print("\n== MODO DE JOGO ==\n")
        print("1. Jogador vs Computador")
        print("2. Jogador vs Jogador")
        
        while True:
            escolha = input("\nEscolha o modo de jogo: ")
            
            if escolha == '1':
                self.modo_computador = True
                self.escolher_simbolo()
                break
            elif escolha == '2':
                self.modo_computador = False
                break
            else:
                print("Opção inválida! Escolha 1 ou 2.")
    
    def escolher_simbolo(self):
        """Permite ao jogador escolher jogar como X ou O"""
        self.limpar_tela()
        print("\n== ESCOLHA SEU SÍMBOLO ==\n")
        print("1. Jogar como X (primeiro a jogar)")
        print("2. Jogar como O (segundo a jogar)")
        
        while True:
            escolha = input("\nEscolha seu símbolo: ")
            
            if escolha == '1':
                self.simbolo_humano = 'X'
                self.simbolo_computador = 'O'
                break
            elif escolha == '2':
                self.simbolo_humano = 'O'
                self.simbolo_computador = 'X'
                # Se o jogador escolher O, o computador (X) começa
                break
            else:
                print("Opção inválida! Escolha 1 ou 2.")

    def menu_principal(self):
        """Exibe o menu principal do jogo"""
        while True:
            self.limpar_tela()
            print("\n== TAPATAN ==\n")
            print("1. Iniciar novo jogo")
            print("2. Regras")
            print("3. Sair")
            
            escolha = input("\nEscolha uma opção: ")
            
            if escolha == '1':
                self.__init__()  # Reinicia o jogo
                self.configurar_modo_jogo()
                self.jogar()
                input("\nPressione Enter para voltar ao menu principal...")
            elif escolha == '2':
                self.mostrar_regras()
                input("\nPressione Enter para voltar ao menu principal...")
            elif escolha == '3':
                print("\nObrigado por jogar Tapatan!")
                break
            else:
                print("Opção inválida!")
                time.sleep(1)
    
    def mostrar_regras(self):
        """Exibe as regras do jogo"""
        self.limpar_tela()
        print("\n== REGRAS DO TAPATAN ==\n")
        print("1. Cada jogador começa com 3 peças já posicionadas no tabuleiro.")
        print("2. Os jogadores se alternam movendo uma de suas peças para uma posição adjacente vazia.")
        print("3. Os movimentos só podem ser feitos ao longo das linhas do tabuleiro.")
        print("4. O objetivo é conseguir três peças em linha (horizontal, vertical ou diagonal).")
        print("5. O jogador que formar uma linha com suas três peças primeiro, vence.")
        print("\nNo início do jogo, o tabuleiro está configurado com:")
        print("- Jogador X: 2 peças do seu lado e 1 do lado oposto")
        print("- Jogador O: 2 peças do seu lado e 1 do lado oposto")