from django.urls import path, include
from rest_framework.routers import DefaultRouter
from configapp.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)


router = DefaultRouter()
router.register(r'actors', ActorModelViewSet, basename='actor')
router.register(r'movies', MovieModelViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/', obtain_auth_token),
    path('movies/year/<int:year>/', MoviesByYearView.as_view(), name='movies-by-year'),
    path('movies/range/', MoviesByYearRangeView.as_view(), name='movies-by-year-range'),
    path('movies/few-actors/', MoviesWithLessActorsView.as_view(), name='movies-few-actors'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path("get/", StraffList.as_view(), name="register"),
    path('post/', StaffRegister.as_view(), name='register'),
    path('api/token/', Login.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
]