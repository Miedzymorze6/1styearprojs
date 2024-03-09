import random

eye_colors = ['brown', 'blue', 'green']
genders = ['male', 'female']
def create_individual():
    return {'eye_color': random.choice(eye_colors), 'gender': random.choice(genders)}

def reproduce(parent1, parent2):
    num_children = random.randint(1, 4)
    children = []
    for _ in range(num_children):
        child = {
            'eye_color': random.choice([parent1['eye_color'], parent2['eye_color']]),
            'gender': random.choice(genders)
        }
        children.append(child)

    return children
def run_simulation(num_generations):
    population = [create_individual() for _ in range(10)]
    for generation in range(1, num_generations + 1):
        print(f"\nGeneration {generation}:")
        random.shuffle(population)
        if len(population) % 2 == 1:
            removed_individual = population.pop()
            print(f"Removed Individual: Eye Color - {removed_individual['eye_color']}, Gender - {removed_individual['gender']}")

        couples = [(population[i], population[i + 1]) for i in range(0, len(population), 2)]
        new_population = []
        for couple in couples:
            children = reproduce(couple[0], couple[1])
            new_population.extend(children)
        population = new_population
        for i, individual in enumerate(population, 1):
            print(f"Individual {i}: Eye Color - {individual['eye_color']}, Gender - {individual['gender']}")
run_simulation(10)
