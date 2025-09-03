from django.urls import path
from configapp.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

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
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', Login.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
]