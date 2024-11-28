from django.urls import path

from . import views

app_name = 'flaws'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_id>/pets/', views.user_pets, name='user_pets'),
    path('<int:user_id>/pets/<int:pk>', views.DetailView.as_view(), name='pet_details'),
    path('admin/', views.admin_view, name='admin'),
    path('admin/petsearch', views.admin_pets_query, name='petsearch')
]