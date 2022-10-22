import json
from django.shortcuts import render
from django.http import HttpResponse
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


def init_game(request):
    with open('connect_four/joeureuse.dat', 'wb') as file:
        pickle.dump(Joueureuse('R'), file)

    with open('connect_four/ai.dat', 'wb') as file:
        pickle.dump(Ai_C4('Y', 'R'), file)

    with open('connect_four/board.dat', 'wb') as file:
        pickle.dump(Board(6, 7), file)
    return HttpResponse("session is set")

def request_access(request):
    colonne = request.POST.get('request_data')
    player = request.POST.get('player')
    board = None

    with open('connect_four/board.dat', 'rb') as file:
        board = pickle.load(file)

    if player == "joeureuse1":
        with open('connect_four/joeureuse.dat', 'rb') as file:
            player = pickle.load(file)
    else:
        with open('connect_four/ai.dat', 'rb') as file:
            player = pickle.load(file)

    if isinstance(player, Ai_C4):
        player.jouer(board)
    else:
        player.jouer(board, colonne)

    with open('connect_four/board.dat', 'wb') as file:
        pickle.dump(board, file)
    
    return HttpResponse("session is set")

def print_id(request):
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