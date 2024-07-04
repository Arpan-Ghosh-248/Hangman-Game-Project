from django.urls import path
from .views import start_new_game, retrieve_game_state, make_guess

urlpatterns = [
    path('new/', start_new_game, name='start_new_game'),
    path('<int:pk>/', retrieve_game_state, name='retrieve_game_state'),
    path('<int:pk>/guess/', make_guess, name='make_guess'),
]
