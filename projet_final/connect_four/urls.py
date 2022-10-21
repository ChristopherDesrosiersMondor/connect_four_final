from django.urls import path
from connect_four import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.request_access , name='request_access'),
]