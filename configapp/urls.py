from django.urls import path
from configapp.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('get/', ActorAll.as_view()),
    path('post/', ActorCreate.as_view()),
    path('put/<int:pk>/', ActorUpdate.as_view()),
    path('delete/<int:pk>/', ActorDelete.as_view()),
    path('auth/', obtain_auth_token),
    path('getM/', MovieAll.as_view()),
    path('postM/', MovieCreate.as_view()),
    path('putM/<int:pk>/', MovieUpdate.as_view()),
    path('deleteM/<int:pk>/', MovieDelete.as_view()),
    path('getC/', CommitMovieAll.as_view()),
    path('postC/', CommitMovieCreate.as_view()),
    path('putC/<int:pk>/', CommitMovieUpdate.as_view()),
    path('deleteC/<int:pk>/', CommitMovieDelete.as_view()),
    path('movies/year/<int:year>/', MoviesByYearView.as_view(), name='movies-by-year'),
    path('movies/range/', MoviesByYearRangeView.as_view(), name='movies-by-year-range'),
    path('movies/few-actors/', MoviesWithLessActorsView.as_view(), name='movies-few-actors'),
    
]