import random
import threading
import time


def criar_tabuleiro(tamanho):
    # Lista de 32 símbolos únicos
    simbolos = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')[:32]
    pares_necessarios = (tamanho * tamanho) // 2
    # Multiplicar a lista de símbolos para garantir que haja símbolos suficientes para pares
    todos_simbolos = (simbolos * (pares_necessarios // 32 + 1))[:pares_necessarios]
    todos_simbolos = todos_simbolos * 2  # Duplicar símbolos para formar pares
    random.shuffle(todos_simbolos)
    return [todos_simbolos[i * tamanho:(i + 1) * tamanho] for i in range(tamanho)]


def mostrar_tabuleiro(tabuleiro, visivel):
    print(" ", end=" ")
    for i in range(len(tabuleiro)):
        print(i, end=" ")
    print()
    for i, linha in enumerate(tabuleiro):
        print(i, end=" ")
        for j, simbolo in enumerate(linha):
            if visivel[i][j]:
                print(simbolo, end=' ')
            else:
                print('*', end=' ')
        print()


def jogo_da_memoria():
    def tempo_acabou():
        nonlocal tempo_esgotado
        time.sleep(180)  # 3 minutos em segundos
        tempo_esgotado = True

    niveis = [(4, 4), (6, 6), (7, 7), (8, 8), (8, 8)]  # Níveis e tamanhos de tabuleiro
    for nivel, (tamanho_linhas, tamanho_colunas) in enumerate(niveis, start=1):
        print(f"\nBem-vindo ao Nível {nivel}!")
        tabuleiro = criar_tabuleiro(tamanho_linhas)
        visivel = [[False] * tamanho_colunas for _ in range(tamanho_linhas)]
        tentativas = 0
        tempo_esgotado = False

        # Inicia a contagem do tempo
        timer_thread = threading.Thread(target=tempo_acabou)
        timer_thread.start()

        while not all(all(linha) for linha in visivel):
            if tempo_esgotado:
                print("Seu tempo acabou, tente novamente.")
                return

            mostrar_tabuleiro(tabuleiro, visivel)
            print("\n" + "-" * (tamanho_colunas * 2 + 1) + "\n")  # Linha de separação

            try:
                x1, y1 = map(int, input("Escolha a primeira carta (linha coluna): ").split())
                x2, y2 = map(int, input("Escolha a segunda carta (linha coluna): ").split())

                # Verificação de coordenadas
                if not (
                        0 <= x1 < tamanho_linhas and 0 <= y1 < tamanho_colunas and 0 <= x2 < tamanho_linhas and 0 <= y2 < tamanho_colunas):
                    print("Coordenadas fora dos limites do tabuleiro. Tente novamente.")
                    continue

                # Verificação de seleção inválida
                if (x1 == x2 and y1 == y2) or visivel[x1][y1] or visivel[x2][y2]:
                    print("Seleção inválida. Tente novamente.")
                    continue

            except ValueError:
                print("Entrada inválida. Por favor, insira as coordenadas no formato 'linha coluna'.")
                continue

            visivel[x1][y1] = True
            visivel[x2][y2] = True
            mostrar_tabuleiro(tabuleiro, visivel)
            print("\n" + "-" * (tamanho_colunas * 2 + 1) + "\n")  # Linha de separação

            if tabuleiro[x1][y1] != tabuleiro[x2][y2]:
                visivel[x1][y1] = False
                visivel[x2][y2] = False

            tentativas += 1

        if tempo_esgotado:
            print("Seu tempo acabou, tente novamente.")
            return
        else:
            print(f"Você venceu o Nível {nivel} em {tentativas} tentativas!")


jogo_da_memoria()