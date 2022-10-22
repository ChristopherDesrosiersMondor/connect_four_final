from django.urls import path
from connect_four import views

urlpatterns = [
    path('', views.home_try, name='home'),
    path('test/', views.request_access , name='request_access'),
    path('id/', views.print_id, name = 'print_id'),
    path('init/', views.init_game, name='init')
]