# environment.py
import pygame
import numpy as np

class Environment:
    def __init__(self, num_classes, num_students, num_time_slots):
        self.num_classes = num_classes
        self.num_students = num_students
        self.num_time_slots = num_time_slots

        # Generate class durations (1 or 2 hours) and priorities (1 to 5)
        self.class_durations = np.random.randint(1, 3, size=num_classes)
        self.class_priorities = np.random.randint(1, 6, size=num_classes)

        # Define time slots
        self.time_slots = [f"Slot {i+1}" for i in range(num_time_slots)]

        # Generate student availabilities and preferences
        self.student_availabilities = [
            set(np.random.choice(self.time_slots, size=np.random.randint(5, num_time_slots+1), replace=False))
            for _ in range(num_students)
        ]
        self.student_preferences = [
            {ts: np.random.uniform(0.5, 1.5) for ts in self.time_slots} for _ in range(num_students)
        ]

    def generate_assignments(self):
        #Randomly assign classes to students and time slots for the initial population.
        population = []
        for _ in range(50):  # Population size
            assignment = []
            for class_idx in range(self.num_classes):
                time_slot = np.random.choice(self.time_slots)
                student_idx = np.random.randint(0, self.num_students)
                assignment.append((class_idx, student_idx, time_slot))
            population.append(assignment)
        return population

    def draw_grid(self, screen, font, schedule):
        screen.fill((255, 255, 255))  # Background color

        color_map = [(0, 0, 255 - i * 50) for i in range(5)]  # Color gradient for priorities
        # color_map = [(0, 0, 255), (0, 0, 200), (0, 0, 150), (0, 0, 100), (0, 0, 50), (0, 0, 5)]

        # Set spacing and margins
        cell_size = 60
        margin_left = 150
        margin_top = 100

        # Display time slot names on the top (X-axis labels)
        for col, time_slot in enumerate(self.time_slots):
            ts_text = font.render(f"{time_slot}", True, (0, 0, 0))
            screen.blit(ts_text, (margin_left + col * cell_size + cell_size // 5, margin_top - 30))

        # Draw each student's row with assigned classes
        for row in range(self.num_students):
            # Display student preference on the left of each row
            preference = np.mean(list(self.student_preferences[row].values()))
            preference_text = font.render(f"Preference: {preference:.2f}", True, (0, 0, 0))
            screen.blit(preference_text, (10, margin_top + row * cell_size + cell_size // 3))

            for col, time_slot in enumerate(self.time_slots):
                # Determine if this time slot has a class assigned to the current student
                assigned_class = None
                for class_idx, student_idx, ts in schedule:
                    if student_idx == row and ts == time_slot:
                        assigned_class = class_idx
                        break

                # Set color based on class priority if assigned
                if assigned_class is not None:
                    priority = self.class_priorities[col]
                    color = color_map[priority - 1]
                else:
                    color = (200, 200, 200)  

                # Draw the cell
                cell_rect = pygame.Rect(
                    margin_left + col * cell_size,
                    margin_top + row * cell_size,
                    cell_size,
                    cell_size
                )

               
                
                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # Draw cell border

                # Display class ID and priority within the cell
                priority_text = font.render(f"P{self.class_priorities[col]}", True, (255, 255, 255))
                duration_text = font.render(f"{self.class_durations[col]}h", True, (255, 255, 255))
                screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 5))
                screen.blit(duration_text, (cell_rect.x + 5, cell_rect.y + 25))

                