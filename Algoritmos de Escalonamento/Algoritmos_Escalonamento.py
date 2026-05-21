import random

class Processo:
    def __init__(self, tempo_execucao, tempo_chegada, prioridade):
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade
        self.tempo_espera = 0
        self.primeiro_inicio = None  # Usado pelo algoritmos preemptivos

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

        # Se nenhum processo está pronto, pula para a chegada com uma única linha
        if tempo < p.tempo_chegada:
            print(f"Tempo[{p.tempo_chegada - 1}]: Nenhum processo está pronto")
            tempo = p.tempo_chegada

        p.tempo_espera = tempo - p.tempo_chegada

        while p.tempo_restante > 0:
            p.tempo_restante -= 1
            print(f"Tempo[{tempo}]: Processo[{i}] Restante={p.tempo_restante}")
            tempo += 1

    print()

    soma = 0
    for i in range(len(processos)):
        print(f"Processo[{i}]: Tempo de espera={processos[i].tempo_espera}")
        soma += processos[i].tempo_espera

    media = soma / len(processos)
    print(f"Tempo médio de espera: {media}\n")


def sjf_nao_preemptivo(processos):
    n = len(processos)
    tempo = 0
    concluidos = [False] * n # Lista de processos concluídos, inicialmente com todos os espaços como False
    num_concluidos = 0

    print()

    while num_concluidos < n:
        # Processos que já chegaram e ainda não foram concluídos
        disponiveis = [
            i for i in range(n)
            if not concluidos[i] and processos[i].tempo_chegada <= tempo
        ]

        if not disponiveis:
            # Pula para a próxima chegada imprimindo uma única linha de ocioso
            proxima_chegada = min(
                processos[i].tempo_chegada for i in range(n) if not concluidos[i]
            )
            print(f"Tempo[{proxima_chegada - 1}]: Nenhum processo está pronto")
            tempo = proxima_chegada
            continue

        # Escolhe o de menor tempo de execução original. Em caso de empate, menor índice - Uso de "lambda" para a chave sugerido por IA
        idx = min(disponiveis, key=lambda i: processos[i].tempo_execucao)
        p = processos[idx]

        p.tempo_espera = tempo - p.tempo_chegada

        # Executa até o fim (não-preemptivo); Imprime antes de incrementar
        while p.tempo_restante > 0:
            p.tempo_restante -= 1
            print(f"Tempo[{tempo}]: Processo[{idx}] Restante={p.tempo_restante}")
            tempo += 1

        concluidos[idx] = True
        num_concluidos += 1

    print()

    soma = 0
    for i in range(n):
        print(f"Processo[{i}]: Tempo de espera={processos[i].tempo_espera}")
        soma += processos[i].tempo_espera

    media = soma / n
    print(f"Tempo médio de espera: {media}\n")


def sjf_preemptivo(processos):
    n = len(processos)
    tempo = 0
    concluidos = [False] * n # Lista de processos concluídos, inicialmente com todos os espaços como False
    num_concluidos = 0

    print()

    while num_concluidos < n:
        # Processos disponíveis: já chegaram e não foram concluídos
        disponiveis = [
            i for i in range(n)
            if not concluidos[i] and processos[i].tempo_chegada <= tempo
        ]

        if not disponiveis:
            # Pula para a próxima chegada imprimindo uma única linha de ocioso
            proxima_chegada = min(
                processos[i].tempo_chegada for i in range(n) if not concluidos[i]
            )
            print(f"Tempo[{proxima_chegada - 1}]: Nenhum processo está pronto")
            tempo = proxima_chegada
            continue

        # Escolhe o processo com menor tempo RESTANTE; em empate, menor índice - Uso de "lambda" para a chave sugerido por IA
        idx = min(disponiveis, key=lambda i: processos[i].tempo_restante)
        p = processos[idx]

        # Registra o tempo de espera na primeira vez que o processo executa
        if p.primeiro_inicio is None:
            p.primeiro_inicio = tempo
            p.tempo_espera = tempo - p.tempo_chegada

        # Executa por 1 unidade de tempo; imprime antes de incrementar
        p.tempo_restante -= 1
        print(f"Tempo[{tempo}]: Processo[{idx}] Restante={p.tempo_restante}")
        tempo += 1

        if p.tempo_restante == 0:
            concluidos[idx] = True
            num_concluidos += 1

    print()

    soma = 0
    for i in range(n):
        print(f"Processo[{i}]: Tempo de espera={processos[i].tempo_espera}")
        soma += processos[i].tempo_espera

    media = soma / n
    print(f"Tempo médio de espera: {media}\n")


def prioridade_nao_preemptivo(processos):
    n = len(processos)
    tempo = 0
    concluidos = [False] * n # Lista de processos concluídos, inicialmente com todos os espaços como False
    num_concluidos = 0

    print()

    while num_concluidos < n:
        # Processos que já chegaram e ainda não foram concluídos
        disponiveis = [
            i for i in range(n)
            if not concluidos[i] and processos[i].tempo_chegada <= tempo
        ]

        if not disponiveis:
            # Pula para a próxima chegada imprimindo uma única linha de ocioso
            proxima_chegada = min(
                processos[i].tempo_chegada for i in range(n) if not concluidos[i]
            )
            print(f"Tempo[{proxima_chegada - 1}]: Nenhum processo está pronto")
            tempo = proxima_chegada
            continue

        # Escolhe o de maior prioridade; em empate, menor índice - Uso de "lambda" para a chave sugerido por IA
        idx = max(disponiveis, key=lambda i: (processos[i].prioridade, -i))
        p = processos[idx]

        p.tempo_espera = tempo - p.tempo_chegada

        # Executa até o fim (não-preemptivo)
        while p.tempo_restante > 0:
            p.tempo_restante -= 1
            print(f"Tempo[{tempo}]: Processo[{idx}] Restante={p.tempo_restante}")
            tempo += 1

        concluidos[idx] = True
        num_concluidos += 1

    print()

    soma = 0
    for i in range(n):
        print(f"Processo[{i}]: Tempo de espera={processos[i].tempo_espera}")
        soma += processos[i].tempo_espera

    media = soma / n
    print(f"Tempo médio de espera: {media}\n")


def prioridade_preemptivo(processos):
    n = len(processos)
    tempo = 0
    concluidos = [False] * n #Lista de processos concluídos, inicialmente com todos os espaços como False
    num_concluidos = 0

    print()

    while num_concluidos < n:
        # Processos disponíveis: já chegaram e não foram concluídos
        disponiveis = [
            i for i in range(n)
            if not concluidos[i] and processos[i].tempo_chegada <= tempo
        ]

        if not disponiveis:
            # Pula para a próxima chegada imprimindo uma única linha de ocioso
            proxima_chegada = min(
                processos[i].tempo_chegada for i in range(n) if not concluidos[i]
            )
            print(f"Tempo[{proxima_chegada - 1}]: Nenhum processo está pronto")
            tempo = proxima_chegada
            continue

        # Escolhe o processo com maior prioridade; em empate, menor índice - Uso de "lambda" para a chave sugerido por IA
        idx = max(disponiveis, key=lambda i: (processos[i].prioridade, -i))
        p = processos[idx]

        # Registra o tempo de espera na primeira vez que o processo executa
        if p.primeiro_inicio is None:
            p.primeiro_inicio = tempo
            p.tempo_espera = tempo - p.tempo_chegada

        # Executa por 1 unidade de tempo
        p.tempo_restante -= 1
        print(f"Tempo[{tempo}]: Processo[{idx}] Restante={p.tempo_restante}")
        tempo += 1

        if p.tempo_restante == 0:
            concluidos[idx] = True
            num_concluidos += 1

    print()

    soma = 0
    for i in range(n):
        print(f"Processo[{i}]: Tempo de espera={processos[i].tempo_espera}")
        soma += processos[i].tempo_espera

    media = soma / n
    print(f"Tempo médio de espera: {media}\n")


def round_robin(processos):
    slice = int(input("Escolha o time slice: "))

    n = len(processos)
    tempo = 0
    num_concluidos = 0
    fila = [] # Fila de prontos (índices dos processos)
    adicionados = set() # Controla quais processos já entraram na fila

    print()

    # Adiciona imediatamente processos que chegam no instante 0
    for i in range(n):
        if processos[i].tempo_chegada <= tempo:
            fila.append(i)
            adicionados.add(i)

    while num_concluidos < n:
        # CPU ociosa: nenhum processo disponível ainda
        if not fila:
            proxima_chegada = min(
                processos[i].tempo_chegada for i in range(n) if i not in adicionados
            )
            print(f"Tempo[{proxima_chegada - 1}]: Nenhum processo está pronto")
            tempo = proxima_chegada
            # Enfileira todos os que chegam neste instante
            for i in range(n):
                if processos[i].tempo_chegada <= tempo and i not in adicionados:
                    fila.append(i)
                    adicionados.add(i)
            continue

        idx = fila.pop(0)
        p = processos[idx]

        # Registra o tempo de espera na primeira execução do processo
        if p.primeiro_inicio is None:
            p.primeiro_inicio = tempo
            p.tempo_espera = tempo - p.tempo_chegada

        # Executa por no máximo de ticks na timeslice
        ticks = min(slice, p.tempo_restante)
        for tick in range(ticks):
            p.tempo_restante -= 1
            print(f"Tempo[{tempo}]: Processo[{idx}] Restante={p.tempo_restante}")
            tempo += 1

            # Verifica novos processos a cada tick
            for i in range(n):
                if processos[i].tempo_chegada <= tempo and i not in adicionados:
                    fila.append(i)
                    adicionados.add(i)

        if p.tempo_restante == 0:
            num_concluidos += 1
        else:
            # Processo não terminou: volta ao fim da fila
            fila.append(idx)

    print()

    soma = 0
    for i in range(n):
        print(f"Processo[{i}]: Tempo de espera={processos[i].tempo_espera}")
        soma += processos[i].tempo_espera

    media = soma / n
    print(f"Tempo médio de espera: {media}\n")


def resetar_processos(processos):
    for p in processos:
        p.tempo_restante = p.tempo_execucao
        p.tempo_espera = 0
        p.primeiro_inicio = None


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
              "9 - Sair\n"
              "Opção: "))

        if op == 1:
            resetar_processos(processos)
            fcfs(processos)

        elif op == 2:
            resetar_processos(processos)
            sjf_preemptivo(processos)

        elif op == 3:
            resetar_processos(processos)
            sjf_nao_preemptivo(processos)

        elif op == 4:
            resetar_processos(processos)
            prioridade_preemptivo(processos)

        elif op == 5:
            resetar_processos(processos)
            prioridade_nao_preemptivo(processos)

        elif op == 6:
            resetar_processos(processos)
            round_robin(processos)

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