# run.py
import pygame
import numpy as np
from agent import Student
from environment import Environment
import random

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800  # Increased height to accommodate updates below the grid
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Class Schedule Visualization")
font = pygame.font.Font(None, 24)

# Environment setup
num_classes = 10
num_students = 5
num_time_slots = 8
environment = Environment(num_classes, num_students, num_time_slots)
initial_population = environment.generate_assignments()

# Initialize students
students = [
    Student(
        id=i,
        availability=environment.student_availabilities[i],
        preferences=environment.student_preferences[i]
    )
    for i in range(num_students)
]

# Genetic Algorithm parameters
population_size = 50
mutation_rate = 0.1
n_generations = 100
generation_delay = 500  # Delay (milliseconds) between each generation for visualization

# Updates list to display below the grid
updates = []
max_updates = 5  # Max number of updates to display at once

# Genetic Algorithm functions
def fitness(individual):
    conflict_penalty = 0
    preference_penalty = 0

    # Reset student schedules
    for student in students:
        student.reset_schedule()

    # Build student schedules and check for conflicts
    schedule_per_student = {student.id: {} for student in students}  # {student_id: {time_slot: class_id}}
    for (class_idx, student_idx, time_slot) in individual:
        student = students[student_idx]
        class_priority = environment.class_priorities[class_idx]

        # Assign class to student
        if time_slot in schedule_per_student[student_idx]:
            # Conflict: student already has a class at this time slot
            conflict_penalty += 1
        else:
            schedule_per_student[student_idx][time_slot] = class_idx
            student.assign_class(class_idx, time_slot)

            # Check if student is available
            if time_slot not in student.availability:
                conflict_penalty += 1

            # Preference penalty
            preference = student.preferences.get(time_slot, 1)
            if preference == 0:
                preference = 1  # Avoid division by zero
            if preference < 3:
                preference_penalty += 1 / preference

    fitness_value = conflict_penalty + preference_penalty
    return fitness_value

def selection(population):
    # Select individuals based on fitness (roulette wheel selection)
    fitnesses = [fitness(individual) for individual in population]
    max_fitness = max(fitnesses)
    total_diffs = sum(max_fitness - f for f in fitnesses)
    if total_diffs == 0:
        selection_probs = [1 / len(fitnesses)] * len(fitnesses)
    else:
        selection_probs = [(max_fitness - f) / total_diffs for f in fitnesses]
    selected_indices = np.random.choice(len(population), size=population_size // 2, p=selection_probs, replace=False)
    return [population[i] for i in selected_indices]

def crossover(parent1, parent2):
    point = random.randint(1, num_classes - 1)
    return parent1[:point] + parent2[point:]

def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            # Reassign class to different student or time slot
            student_idx = np.random.randint(0, num_students)
            time_slot = random.choice(environment.time_slots)
            individual[i] = (individual[i][0], student_idx, time_slot)
    return individual

# Initialize population
population = initial_population

# Visualization loop
running = True
best_solution = None
best_fitness = float('inf')
generation_count = 0

while running and generation_count < n_generations:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Genetic Algorithm per generation
    selected = selection(population)
    next_generation = []
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_generation.append(child)

    # Update population with next generation
    population = next_generation

    # Find the best solution in the current generation
    current_best = min(population, key=fitness)
    current_fitness = fitness(current_best)
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        best_solution = current_best

    # Draw current generation's best solution on the grid
    environment.draw_grid(screen, font, best_solution)

    # Display generation and fitness info on the right panel
    generation_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
    fitness_text = font.render(f"Best Fitness (Current): {best_fitness:.2f}", True, (0, 0, 0))
    max_fitness_text = font.render(f"Max Fitness Achieved: {best_fitness:.2f}", True, (0, 0, 0))
    screen.blit(generation_text, (SCREEN_WIDTH - 250, 50))
    screen.blit(fitness_text, (SCREEN_WIDTH - 250, 80))
    screen.blit(max_fitness_text, (SCREEN_WIDTH - 250, 110))

    # Add update for the current generation to the updates list
    update_text = f"Generation {generation_count + 1}: Best Fitness = {best_fitness:.2f}"
    updates.append(update_text)
    if len(updates) > max_updates:
        updates.pop(0)  # Remove the oldest update if we exceed the display limit

    # Display the list of updates below the grid
    update_start_y = 650  # Starting Y position below the grid
    for i, update in enumerate(updates):
        update_surface = font.render(update, True, (0, 0, 0))
        screen.blit(update_surface, (50, update_start_y + i * 25))

    pygame.display.flip()
    pygame.time.delay(generation_delay)

    generation_count += 1

# Keep window open after completion
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()