from django.urls import path
from . import views


urlpatterns = [
    path ('', views.index, name='index'),
    path ('login', views.login, name='login'),
    path ('signup', views.signup, name='signup'),
    path ('logout', views.logout, name='logout'),
    path('top-artists/', views.top_artists, name='top_artists'),
    path('music/<str:pk>/', views. music, name='music'),
]