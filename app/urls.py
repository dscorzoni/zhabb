from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('auth/', views.Auth.as_view(), name='auth'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('habits/', views.HabitsMain.as_view(), name='habits'),
]