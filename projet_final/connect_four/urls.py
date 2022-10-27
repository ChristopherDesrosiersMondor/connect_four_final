from django.urls import path
from connect_four import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jeu/', views.home_try, name='jeu'),
    path('jeu/jouer/', views.jouer , name='request_access'),
    path('reglement/', views.reglement, name='reglement')
]