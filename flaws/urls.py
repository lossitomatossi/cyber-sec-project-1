from django.urls import path

from . import views

app_name = 'flaws'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_id>/pets/', views.user_pets, name='user_pets'),
]