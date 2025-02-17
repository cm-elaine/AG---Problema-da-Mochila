import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Função de Força Bruta
def knapsack_brute_force(capacidade, pesos, valores):
    n = len(pesos)
    max_valor = 0
    melhor_combinacao = []
    # Gerar todas as combinações possíveis (2^n combinações)
    for i in range(2**n):
        combinacao = []
        peso_total = 0
        valor_total = 0
        # Verificar quais itens estão na combinação atual
        for j in range(n):
            if (i >> j) & 1:
                combinacao.append(j)
                peso_total += pesos[j]
                valor_total += valores[j]
        # Verificar se a combinação é válida e se o valor é o maior até agora
        if peso_total <= capacidade and valor_total > max_valor:
            max_valor = valor_total
            melhor_combinacao = combinacao
    return max_valor, melhor_combinacao

# Função Aleatória
def knapsack_random(capacidade, pesos, valores, num_tentativas=1000):
    n = len(pesos)
    max_valor = 0
    melhor_combinacao = []
    for _ in range(num_tentativas):
        combinacao = []
        peso_total = 0
        valor_total = 0
        # Escolher aleatoriamente quais itens incluir
        for j in range(n):
            if random.random() < 0.5:  # 50% de chance de incluir o item
                combinacao.append(j)
                peso_total += pesos[j]
                valor_total += valores[j]
        # Verificar se a combinação é válida e se o valor é o maior até agora
        if peso_total <= capacidade and valor_total > max_valor:
            max_valor = valor_total
            melhor_combinacao = combinacao
    return max_valor, melhor_combinacao

# Função para calcular a aptidão (fitness) de um indivíduo
def fitness(individuo, pesos, valores, capacidade):
    peso_total = sum(pesos[i] for i in range(len(individuo)) if individuo[i])
    valor_total = sum(valores[i] for i in range(len(individuo)) if individuo[i])
    if peso_total > capacidade:
        return 0  # Penalidade para soluções inválidas
    return valor_total

# Função para criar uma população inicial aleatória
def criar_populacao(tamanho_populacao, n):
    return [[random.choice([0, 1]) for _ in range(n)] for _ in range(tamanho_populacao)]

# Função para realizar o crossover entre dois pais
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

# Função para aplicar mutação em um indivíduo
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]  # Inverter o bit
    return individuo

# Função principal do algoritmo genético personalizado
def knapsack_genetico_personalizado(capacidade, pesos, valores, tamanho_populacao=100, geracoes=100, taxa_mutacao=0.01):
    n = len(pesos)
    populacao = criar_populacao(tamanho_populacao, n)
    for _ in range(geracoes):
        # Avaliar aptidão
        populacao = sorted(populacao, key=lambda x: fitness(x, pesos, valores, capacidade), reverse=True)
        # Selecionar os melhores indivíduos
        nova_populacao = populacao[:tamanho_populacao // 2]
        # Gerar novos indivíduos por crossover
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.choices(populacao[:tamanho_populacao // 2], k=2)
            filho1, filho2 = crossover(pai1, pai2)
            nova_populacao.append(mutacao(filho1, taxa_mutacao))
            nova_populacao.append(mutacao(filho2, taxa_mutacao))
        populacao = nova_populacao
    # Retornar o melhor indivíduo
    melhor_individuo = max(populacao, key=lambda x: fitness(x, pesos, valores, capacidade))
    max_valor = fitness(melhor_individuo, pesos, valores, capacidade)
    melhor_combinacao = [i for i in range(n) if melhor_individuo[i]]
    return max_valor, melhor_combinacao

# Configuração do DEAP para o Algoritmo Genético
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Atributos: Cada gene é 0 ou 1 (indicando se o item está na mochila)
toolbox.register("attr_bool", random.randint, 0, 1)

def evaluate(individual):
    total_weight = sum(ind * peso for ind, peso in zip(individual, pesos))
    total_value = sum(ind * valor for ind, valor in zip(individual, valores))
    if total_weight > capacidade:
        return (0,)  # Penaliza soluções inválidas
    return (total_value,)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Função para executar o AG com DEAP
def run_genetic_algorithm():
    random.seed(42)
    population = toolbox.population(n=50)
    ngen = 50  # Número de gerações
    cxpb = 0.7  # Probabilidade de crossover
    mutpb = 0.2  # Probabilidade de mutação

    # Estatísticas para visualização
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    # Executar o AG
    population, logbook = algorithms.eaSimple(
        population, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, stats=stats, verbose=True
    )

    # Encontrar o melhor indivíduo
    best_individual = tools.selBest(population, k=1)[0]
    best_fitness = best_individual.fitness.values[0]
    return best_fitness, best_individual, logbook

# Visualização da evolução
def plot_evolution(logbook):
    gen = logbook.select("gen")
    avg_fitness = logbook.select("avg")
    max_fitness = logbook.select("max")

    plt.figure(figsize=(10, 6))
    plt.plot(gen, avg_fitness, label="Fitness Médio")
    plt.plot(gen, max_fitness, label="Melhor Fitness", linestyle="--")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.title("Evolução do Fitness ao Longo das Gerações")
    plt.legend()
    plt.grid()
    plt.show()

# Exemplo de uso
if __name__ == "__main__":
    capacidade = 50
    pesos = [10, 20, 30]
    valores = [60, 100, 120]

    # Força Bruta
    print("Executando Força Bruta...")
    max_valor_brute_force, melhor_combinacao_brute_force = knapsack_brute_force(capacidade, pesos, valores)
    print("Força Bruta:")
    print(f"Valor máximo: {max_valor_brute_force}")
    print(f"Itens selecionados: {melhor_combinacao_brute_force}")

    # Aleatório
    print("\nExecutando Aleatório...")
    max_valor_random, melhor_combinacao_random = knapsack_random(capacidade, pesos, valores, num_tentativas=1000)
    print("Aleatório:")
    print(f"Valor máximo: {max_valor_random}")
    print(f"Itens selecionados: {melhor_combinacao_random}")

    # Algoritmo Genético Personalizado
    print("\nExecutando Algoritmo Genético Personalizado...")
    max_valor_ag_personalizado, melhor_combinacao_ag_personalizado = knapsack_genetico_personalizado(capacidade, pesos, valores)
    print("Algoritmo Genético Personalizado:")
    print(f"Valor máximo: {max_valor_ag_personalizado}")
    print(f"Itens selecionados: {melhor_combinacao_ag_personalizado}")

    # Algoritmo Genético com DEAP
    print("\nExecutando Algoritmo Genético com DEAP...")
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(pesos))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    best_fitness_ag, best_individual_ag, logbook = run_genetic_algorithm()
    print("\nAlgoritmo Genético com DEAP:")
    print(f"Valor máximo: {best_fitness_ag}")
    print(f"Itens selecionados: {[i for i, gene in enumerate(best_individual_ag) if gene == 1]}")

    # Plotar a evolução do AG com DEAP
    plot_evolution(logbook)