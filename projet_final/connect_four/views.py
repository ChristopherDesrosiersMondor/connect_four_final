import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from connect_four.jeu import *
import pickle
# Create your views here.
# https://www.javatpoint.com/django-session

def home(request):
    return render(
        request,
        'connect_four/base.html'
    )

def home_try(request):
    return render(
        request,
        'connect_four/page_jeu.html'
    )

def jouer(request):
    matrice = json.loads(request.GET.get('matrice'))

    ai  = Ai_C4('R', 'Y')

    board = Board(6, 7)
    for i in range(board.rangees):
        for j in range(board.colonnes):
            board.matrice_jeu[i][j].valeur = matrice[i][j]

    colonne = ai.jouer(board)

    win, winner = board.check_for_win()

    response = JsonResponse(colonne, safe=False)
    return response

def print_state(request):
    board = None

    with open('connect_four/board.dat', 'rb') as file:
        board = pickle.load(file)

    print = str(board)
    return render(
    request,
    'connect_four/base.html',
    {
        'print': print
    }
    )