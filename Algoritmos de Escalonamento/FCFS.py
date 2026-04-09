import random

class Processo:
    def __init__(self, tempo_execucao, tempo_chegada, prioridade):
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade
        self.tempo_espera = 0

    def __str__(self):
        return (f"Tempo de execução={self.tempo_execucao} "
                f"Tempo restante={self.tempo_restante} "
                f"Tempo de chegada={self.tempo_chegada} "
                f"Prioridade={self.prioridade}")


def gerar_processos(aleatorio):
    processos = []

    if aleatorio:
        qtd = random.randint(2, 5)
        print(f"\nQuantidade de processos gerada: {qtd}")
    else:
        qtd = int(input("Quantidade de processos: "))

    for i in range(qtd):
        if aleatorio:
            tempo_exec = random.randint(2, 10)
            tempo_chegada = random.randint(0, 10)
            prioridade = random.randint(1, 15)
        else:
            print(f"\nProcesso[{i}]")
            tempo_exec = int(input("Tempo de execução: "))
            tempo_chegada = int(input("Tempo de chegada: "))
            prioridade = int(input("Prioridade: "))

        processos.append(Processo(tempo_exec, tempo_chegada, prioridade))

    return processos


def imprimir_processos(processos):
    print()
    for i in range(len(processos)):
        print(f"Processo[{i}]: {processos[i]}")


def fcfs(processos):
    tempo = 0

    print()

    for i in range(len(processos)):
        p = processos[i]

        if tempo < p.tempo_chegada:
            while tempo < p.tempo_chegada:
                tempo += 1
                print(f"Tempo[{tempo}]: Nenhum processo está pronto")

        p.tempo_espera = tempo - p.tempo_chegada

        while p.tempo_restante > 0:
            tempo += 1
            p.tempo_restante -= 1
            print(f"Tempo[{tempo}]: Processo[{i}] Restante={p.tempo_restante}")

    print()

    soma = 0
    for i in range(len(processos)):
        print(f"Processo[{i}]: Tempo de espera={processos[i].tempo_espera}")
        soma += processos[i].tempo_espera

    media = soma / len(processos)
    print(f"Tempo médio de espera: {media}\n")


def resetar_processos(processos):
    for p in processos:
        p.tempo_restante = p.tempo_execucao
        p.tempo_espera = 0


def menu():
    aleatorio = int(input("Será aleatório? (1=Sim 0=Não): "))

    processos = gerar_processos(aleatorio == 1)

    while True:
        op = int(input("\n---Escolha o algoritmo---\n"
              "1 - FCFS\n"
              "2 - SJF Preemptivo\n"
              "3 - SJF Não Preemptivo\n"
              "4 - Prioridade Preemptivo\n"
              "5 - Prioridade Não Preemptivo\n"
              "6 - Round Robin\n"
              "7 - Imprimir processos\n"
              "8 - Popular processos novamente\n"
              "9 - Sair\n" \
              "Opção: "))

        if op == 1:
            resetar_processos(processos)
            fcfs(processos)

        elif op in [2, 3, 4, 5, 6]:
            print("\nAlgoritmo ainda não implementado")

        elif op == 7:
            imprimir_processos(processos)

        elif op == 8:
            aleatorio = int(input("\nSerá aleatório? (1=Sim 0=Não): "))
            processos = gerar_processos(aleatorio == 1)

        elif op == 9:
            break

        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    menu()