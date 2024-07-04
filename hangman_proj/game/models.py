from django.db import models

class Game(models.Model):
    WORDS = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]
    
    word = models.CharField(max_length=50)
    state = models.CharField(max_length=10, default='InProgress')
    incorrect_guesses = models.IntegerField(default=0)
    max_incorrect_guesses = models.IntegerField()

    def __str__(self):
        return f'Game {self.id}: {self.word}'

class Guess(models.Model):
    game = models.ForeignKey(Game, related_name='guesses', on_delete=models.CASCADE)
    character = models.CharField(max_length=1)

    def __str__(self):
        return f'Guess {self.character} for Game {self.game.id}'
