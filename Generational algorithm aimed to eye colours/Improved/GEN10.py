import random

# Define allele combinations and their corresponding eye colors
allele_eye_color = {
    ('A', 'A'): 'brown',
    ('A', 'B'): 'brown',
    ('A', 'G'): 'brown',
    ('B', 'B'): 'blue',
    ('B', 'G'): 'blue',
    ('G', 'G'): 'green',
}

genders = ['male', 'female']

def create_individual():
    chromosomes = sorted(random.choices(['A', 'B', 'G'], k=2))
    fitness = random.uniform(0, 1)  # Random fitness value between 0 and 1
    return {'chromosomes': chromosomes, 'gender': random.choice(genders), 'fitness': fitness}

def reproduce(parent1, parent2):
    num_children = random.randint(1, 3)
    for _ in range(num_children):
        child_chromosomes = [random.choice(pair) for pair in zip(parent1['chromosomes'], parent2['chromosomes'])]
        child_gender = random.choice(genders)
        fitness = (parent1['fitness'] + parent2['fitness']) / 2  # Average fitness of parents
        yield {'chromosomes': child_chromosomes, 'gender': child_gender, 'fitness': fitness}

def eye_color_from_chromosomes(chromosomes):
    if chromosomes[0] == chromosomes[1]:  # If the chromosomes are the same, return the corresponding eye color
        return allele_eye_color.get((chromosomes[0], chromosomes[1]), 'unknown')
    elif 'B' in chromosomes and 'G' in chromosomes:  # If 'B' and 'G' are present, randomize between blue and green
        return random.choice(['blue', 'green'])
    else:  # Otherwise, return brown
        return 'brown'

def calculate_eye_color_distribution(population):
    eye_color_counts = {'brown': 0, 'blue': 0, 'green': 0}
    for individual in population:
        eye_color = eye_color_from_chromosomes(individual['chromosomes'])
        eye_color_counts[eye_color] += 1
    return eye_color_counts

def run_simulation(num_generations, force_kill_factor):
    population = [create_individual() for _ in range(100)]
    for generation in range(1, num_generations + 1):
        print("-------------------------------------------------------------------------------------")
        print(f"\nGeneration {generation}:")
        if len(population) % 2 == 1:
            population.pop()  # Remove one individual if the population size is odd

        # Applying force kill factor based on fitness
        population.sort(key=lambda x: x['fitness'], reverse=True)  # Sort population by fitness (higher is better)
        num_removed_individuals = int(len(population) * force_kill_factor)
        for _ in range(num_removed_individuals):
            population.pop()  # Remove the least fit individuals

        # Check if the population size is still even
        if len(population) % 2 == 1:
            population.pop()  # Remove one individual if the population size is odd after force kill

        mating_pairs = [(population[i], population[i + 1]) for i in range(0, len(population), 2)]

        # First 3 males mate with 2 females each
        male_parents = [parent for parent in population if parent['gender'] == 'male'][:3]
        female_parents = [parent for parent in population if parent['gender'] == 'female']
        for male_parent in male_parents:
            for _ in range(2):
                female_parent = random.choice(female_parents)
                for child in reproduce(male_parent, female_parent):
                    population.append(child)

        # Remove last 3 individuals due to low fitness
        for _ in range(3):
            population.pop()

        eye_color_distribution = calculate_eye_color_distribution(population)
        print("Eye Color Distribution:", eye_color_distribution)

        num_new_individuals = len(population)
        print("Number of New Individuals:", num_new_individuals)

        for i, (parent1, parent2) in enumerate(mating_pairs, 1):
            print(f"Mating {i}:")
            print(f"Parent 1: Chromosomes - {parent1['chromosomes']}, Gender - {parent1['gender']}, Fitness - {parent1['fitness']}")
            print(f"Parent 2: Chromosomes - {parent2['chromosomes']}, Gender - {parent2['gender']}, Fitness - {parent2['fitness']}")
        print("________________")
        for i, individual in enumerate(population, 1):
            eye_color = eye_color_from_chromosomes(individual['chromosomes'])
            print(
                f"Individual {i}: Chromosomes - {individual['chromosomes']}, Eye Color - {eye_color}, Gender - {individual['gender']}, Fitness - {individual['fitness']}")


force_kill_factor = 0.4  # for brown eyes >:)
run_simulation(10, force_kill_factor)

