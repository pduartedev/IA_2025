'''
Ponto de entrada principal para o jogo Tapatan.
'''

from tapatan import Tapatan

def main():
    """Função principal para iniciar o jogo"""
    jogo = Tapatan()
    jogo.menu_principal()

if __name__ == "__main__":
    main()