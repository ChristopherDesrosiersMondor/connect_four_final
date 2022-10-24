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

def jouer(request):
    board = Board(6, 7)
    board.updater_board('Y', board.first_empty_node(4))

    with open('connect_four/board.dat', 'wb') as file:
         pickle.dump(board, file)
    return HttpResponse("session is set")

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