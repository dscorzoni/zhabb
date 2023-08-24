from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('habits/', views.HabitsMainView.as_view(), name='habits'),
    path('habits/check/<int:pk>', views.HabitLogView.as_view(), name='habits-check'),
    path('habits/new/', views.NewHabit.as_view(), name='new-habit'),
    path('newuser/', views.NewUser.as_view(), name='newuser'),
]