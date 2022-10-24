from django.urls import path
from connect_four import views

urlpatterns = [
    path('', views.home_try, name='home'),
    path('jouer/', views.jouer , name='request_access'),
    path('board_state/', views.print_state, name = 'print_state'),
]