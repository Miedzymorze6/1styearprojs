import random
import string

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

def generate_unique_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_individual():
    chromosomes = sorted(random.choices(['A', 'B', 'G'], k=2))
    fitness = random.uniform(0, 1)  # Random fitness value between 0 and 1
    return {'id': generate_unique_id(), 'chromosomes': chromosomes, 'gender': random.choice(genders), 'fitness': fitness}

def reproduce(parent1, parent2):
    num_children = random.randint(1, 3)
    for _ in range(num_children):
        child_chromosomes = [random.choice(pair) for pair in zip(parent1['chromosomes'], parent2['chromosomes'])]
        child_gender = random.choice(genders)
        fitness = (parent1['fitness'] + parent2['fitness']) / 2  # Average fitness of parents
        yield {'id': generate_unique_id(), 'chromosomes': child_chromosomes, 'gender': child_gender, 'fitness': fitness}

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
    population = [create_individual() for _ in range(10)]
    for generation in range(1, num_generations + 1):
        print("-------------------------------------------------------------------------------------")
        print(f"\nGeneration {generation}:")
        
        # Calculate average fitness
        total_fitness = sum(individual['fitness'] for individual in population)
        average_fitness = total_fitness / len(population) if population else 0
        
        # Randomly remove individuals below average fitness with a 50% chance
        population = [individual for individual in population if individual['fitness'] >= average_fitness or random.random() > 0.5]
        
        # Remove brown-eyed individuals with a chance determined by force_kill_factor
        population = [individual for individual in population if eye_color_from_chromosomes(individual['chromosomes']) != 'brown' or random.random() > force_kill_factor]
        
        # Select mating pairs
        if len(population) < 10:
            # If population size is less than 10, allow multiple individuals to mate
            mating_pairs = [(random.choice(population), random.choice(population)) for _ in range(len(population) // 2)]
        else:
            mating_pairs = [(random.choice(population), random.choice(population)) for _ in range(len(population) // 2)]
        
        # Handle odd population size
        while len(mating_pairs) * 2 < len(population):
            # If population size is odd, randomly select two individuals to mate
            individual1 = random.choice(population)
            individual2 = random.choice(population)
            mating_pairs.append((individual1, individual2))
        
        # Generate offspring from mating pairs
        children = []
        for parent1, parent2 in mating_pairs:
            children.extend(reproduce(parent1, parent2))
            print(f"Mating Pair: Male - ID {parent1['id']}, Female - ID {parent2['id']}")
            for i, child in enumerate(children[-3:], 1):
                eye_color = eye_color_from_chromosomes(child['chromosomes'])
                print(
                    f"Child {i}: ID - {child['id']}, Chromosomes - {child['chromosomes']}, Eye Color - {eye_color}, Gender - {child['gender']}, Fitness - {child['fitness']}")
        
        # Add children to population
        population.extend(children)

        # Calculate eye color distribution
        eye_color_distribution = calculate_eye_color_distribution(population)
        print("Eye Color Distribution:", eye_color_distribution)

        print("Number of New Individuals:", len(population))

        print("________________")
        for i, individual in enumerate(population, 1):
            eye_color = eye_color_from_chromosomes(individual['chromosomes'])
            print(
                f"Individual {i}: ID - {individual['id']}, Chromosomes - {individual['chromosomes']}, Eye Color - {eye_color}, Gender - {individual['gender']}, Fitness - {individual['fitness']}")


force_kill_factor = 0.09  # for brown eyes >:)
run_simulation(5, force_kill_factor)


