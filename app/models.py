from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    '''
    This model is the base of all habits.
    It allows user to create new habits for tracking throughout the time.
    Example (Go to the gym 4 times per week and perform a complete workout):
        name: Go to the gym
        description: Perform a complete workout
        frequency: weekly
        goal: 4 (times per week)
        date_start: 2023-09-01
        active: true (this goal is active)
    '''
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    frequency = models.CharField(max_length = 100)
    goal = models.IntegerField()
    date_start = models.DateField()
    active = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.user} - {self.name}'

class HabitLog(models.Model):
    '''
    This model specify the habit logged. It's linked to the Habit model.
    '''
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE)
    status = models.BooleanField(default = False)
    date_event = models.DateField()

    def __str__(self):
        return f'{self.habit} - {self.date_event} - {self.status}'