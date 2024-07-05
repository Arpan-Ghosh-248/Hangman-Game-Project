import random
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import math
from .models import Game, Guess


@csrf_exempt
@api_view(['POST'])
def start_new_game(request):
    try:
        # Generate a random word for the game
        word = random.choice(Game.WORDS)
        max_incorrect_guesses = math.ceil(len(word) / 2)
        
        # Create a new game instance
        game = Game.objects.create(word=word, max_incorrect_guesses=max_incorrect_guesses)
        
        # Serialize the game instance to return its ID
        return Response({'id': game.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def retrieve_game_state(request, pk):
    game = get_object_or_404(Game, pk=pk)
    response_data = get_game_state(game)
    return Response(response_data)

@csrf_exempt
@api_view(['POST'])
def make_guess(request, pk):
    game = get_object_or_404(Game, pk=pk)
    character = request.data.get('character').lower()

    # Check if the character has already been guessed
    if character in [guess.character.lower() for guess in game.guesses.all()]:
        response_data = get_game_state(game)
        response_data['message'] = f"Character '{character}' has already been guessed."
        return Response(response_data)

    # Determine if the character is in the word
    correct_guess = False
    for char in game.word.lower():
        if char == character:
            correct_guess = True
            break
    
    # Create a new guess instance
    guess = Guess.objects.create(game=game, character=character)

    # if correct_guess:
    # all_guessed = True
    # for char in game.word.lower():
    #     char_guessed = False
    #     for g in game.guesses.all():
    #         if char == g.character:
    #             char_guessed = True
    #             break
    #     if not char_guessed:
    #         all_guessed = False
    #         break
    # if all_guessed:
    #     game.state = 'Won'
    
    # Update game state based on the guess
    if correct_guess:
        if all(char.lower() in [g.character for g in game.guesses.all()] for char in game.word.lower()):
            game.state = 'Won'
    else:
        game.incorrect_guesses += 1
        max_incorrect_guesses_allowed = math.ceil(len(game.word) / 2)
        if game.incorrect_guesses >= max_incorrect_guesses_allowed:
            game.state = 'Lost'
    
    game.save()
    response_data = get_game_state(game)
    response_data['correct_guess'] = correct_guess
    return Response(response_data)


def get_game_state(game):
    guessed_chars = [g.character for g in game.guesses.all()]
    word_state = ''.join([char if char.lower() in guessed_chars else '_' for char in game.word])
    return {
        'state': game.state,
        'word_state': word_state,
        'incorrect_guesses': game.incorrect_guesses,
        'remaining_incorrect_guesses': game.max_incorrect_guesses - game.incorrect_guesses
    }
