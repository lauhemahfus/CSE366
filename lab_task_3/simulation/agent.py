# agent.py
import numpy as np

class Student:
    def __init__(self, id, availability, preferences):
        self.id = id  # Unique identifier for each student
        self.availability = availability  # Set of available time slots
        self.preferences = preferences  # Dictionary mapping time slots to preference scores
        self.schedule = []  # List of assigned classes (class_id, time_slot)

    def assign_class(self, class_id, time_slot):
        self.schedule.append((class_id, time_slot))

    def reset_schedule(self):
        self.schedule = []

    def total_conflicts(self):
        conflicts = 0
        for class_id, time_slot in self.schedule:
            if time_slot not in self.availability:
                conflicts += 1
        return conflicts