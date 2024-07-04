from rest_framework import serializers
from .models import Game, Guess

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'word', 'state', 'incorrect_guesses', 'max_incorrect_guesses']

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ['game', 'character']