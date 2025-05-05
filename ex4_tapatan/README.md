# Tapatan - Jogo de Tabuleiro com IA

## Sobre o Jogo

Tapatan é uma variação do jogo da velha tradicional, também conhecido como "Three Men's Morris". Em contraste com o jogo da velha padrão, onde os jogadores alternam colocando suas peças no tabuleiro, no Tapatan cada jogador começa com 3 peças já posicionadas no tabuleiro e deve movê-las para formar uma linha (horizontal, vertical ou diagonal).

Esta implementação inclui:
- Modo para dois jogadores humanos
- Modo contra computador com IA baseada no algoritmo Minimax
- Interface de console amigável e intuitiva
- 

Por padrão definimos que nosso estado inicial igual a variante filipina do jogo da velha. Portanto, o tabuleiro inicial será estabelecido como:


```
     0     1     2  
  ┌─────┬─────┬─────┐
0 │  X  │  O  │  X  │
  ├─────┼─────┼─────┤
1 │     │     │     │
  ├─────┼─────┼─────┤
2 │  O  │  X  │  O  │
  └─────┴─────┴─────┘
```


## Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária (apenas bibliotecas padrão do Python)

## Como Instalar e Executar

1. Certifique-se de ter o Python instalado em seu sistema
   - Para verificar, execute no terminal: `python --version` ou `python3 --version`
   - Se não tiver o Python instalado, baixe-o em: https://www.python.org/downloads/

2. Clone ou baixe os arquivos deste projeto
   - Certifique-se de que os quatro arquivos estão no mesmo diretório:
     - `main.py`
     - `tapatan.py`
     - `minimax.py`
     - `estado.py`

3. Execute o jogo:
   ```
   python main.py
   ```
   ou (caso utilize a versão 3 do python)
   ```
   python3 main.py 
   ```

## Estrutura do Projeto

O código está modularizado em quatro arquivos:

- **`main.py`**:    Ponto de entrada para iniciar o jogo
- **`tapatan.py`**: Classe principal do jogo com interface e lógica do jogo
- **`minimax.py`**: Implementação do algoritmo Minimax para a IA
- **`estado.py`**:  Classe que representa o estado do tabuleiro

## Como Jogar

### Regras Básicas
1. Cada jogador tem 3 peças de seu símbolo (X ou O)
2. As peças já estão posicionadas no tabuleiro no início do jogo
3. Os jogadores alternam movendo uma peça para uma posição adjacente vazia
4. Os movimentos só podem ser feitos de maneira vertical ou horizontal do tabuleiro
5. O objetivo é formar uma linha com suas três peças (horizontal, vertical ou diagonal)
6. O jogador que primeiro formar uma linha com suas três peças vence

### Controles
- Você interage com o jogo digitando números correspondentes às opções exibidas
- Para mover uma peça:
  1. Selecione a peça que deseja mover (1-3)
  2. Escolha para onde deseja movê-la dentre as opções disponíveis

### Modos de Jogo
- **Jogador vs Computador**:    Desafie a IA baseada no algoritmo Minimax
- **Jogador vs Jogador**:       Dois jogadores humanos se alternam no mesmo dispositivo

## Algoritmo Minimax

O jogo utiliza o algoritmo Minimax com poda alfa-beta para determinar os movimentos do computador:

- **Minimax**: Algoritmo de tomada de decisão para jogos de soma zero que busca minimizar a possível perda máxima
- **Poda alfa-beta**: Otimização que reduz o número de nós avaliados pelo algoritmo Minimax
- **Função de avaliação**: Avalia o estado atual do tabuleiro para determinar quão favorável é a posição

A IA implementada é bastante forte e considera:
- Controle do centro do tabuleiro
- Formações de "dois-em-linha" (peças que estão a um passo de formar uma linha)
- Proximidade entre peças do mesmo jogador
- Mobilidade (número de movimentos disponíveis)

## Detalhes da Implementação

### Estado do Jogo
- O tabuleiro é uma matriz 3x3
- As conexões definem os movimentos possíveis entre posições
- O controle de turno alterna entre os jogadores X e O

### IA do Computador
- Profundidade de busca fixa (definida em 5 níveis)
- Função de avaliação avançada favorece posições estratégicas
- Poda alfa-beta para otimização e decisões mais rápidas

### Funções Importantes
- `jogador(estado)`:            Retorna o jogador atual
- `acoes(estado)`:              Retorna todos os movimentos possíveis
- `resultado(estado, acao)`:    Retorna o novo estado após um movimento
- `ganhador(estado)`:           Verifica se há um vencedor
- `final(estado)`:              Verifica se o jogo acabou
- `custo(estado)`:              Avalia o valor do estado atual

## Colaboração e Melhorias

Se desejar contribuir ou melhorar este jogo, algumas ideias são:
- Adicionar uma interface gráfica
- Implementar níveis de dificuldade ajustáveis
- Adicionar um sistema de pontuação
- Implementar um modo de jogo em rede para jogar online

## Autores

Este jogo foi desenvolvido como projeto educacional para demonstrar a implementação do algoritmo Minimax em jogos de tabuleiro.

## Licença

Este projeto é de código aberto e pode ser usado livremente para fins educacionais.

---

Divirta-se jogando Tapatan!