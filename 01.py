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

# Função para executar o AG
def run_genetic_algorithm():
    random.seed(42)
    population = toolbox.population(n=20)
    ngen = 20  # Número de gerações
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

    # Algoritmo Genético
    print("\nExecutando Algoritmo Genético...")
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(pesos))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    best_fitness_ag, best_individual_ag, logbook = run_genetic_algorithm()
    print("\nAlgoritmo Genético:")
    print(f"Valor máximo: {best_fitness_ag}")
    print(f"Itens selecionados: {[i for i, gene in enumerate(best_individual_ag) if gene == 1]}")

    # Plotar a evolução do AG
    plot_evolution(logbook)