from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from .make_token import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .add_paginition import CustomPagination
from rest_framework_simplejwt.tokens import RefreshToken

class StaffRegister(APIView):
    # permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            User.objects.create_user(phone_number=data['phone_number'], password=data['password'])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class StraffList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        


class ActorModelViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

class MovieModelViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @action(detail=True, methods = ['POST'])
    def add_actor(self, request, *args, **kwargs):
        actor_id = request.data['actor_id']
        movie = self.get_object()
        movie.actor.add(actor_id)
        movie.save()    
        serializer = MovieSerializers(movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'])
    def remove_actor(self, request, *args, **kwargs):
        actor_id = request.data['actor_id']
        movie = self.get_object()
        movie.actor.remove(actor_id)
        movie.save()
        serializer = MovieSerializers(movie)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET'])
    def list_actors(self, request, *args, **kwargs):
        movie = self.get_object()
        serializer = ActorSerializers(movie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# @api_view(['GET', 'POST'])
# def actor_get_post(request):
#     if request.method=='GET':
#         actors=Actor.objects.all()
#         serializer=ActorSerializers(actors,many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#     elif request.method=='POST':
#         serializer=ActorSerializers(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['PUT'])
# def actor_put(request, pk):
#     actor = get_object_or_404(Actor, pk=pk)
#     serializer = ActorSerializers(actor, data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializers

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    
class MoviesByYearView(APIView):
    def get(self, request, year):
        movies = Movie.objects.filter(year=year)
        serializer = MovieSerializers(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class MoviesByYearRangeView(APIView):
        def get(self, request):
            start_year = request.query_params.get('start')
            end_year = request.query_params.get('end')

            if not start_year or not end_year:
                return Response({"error": "start va end yillarni kiriting"}, status=status.HTTP_400_BAD_REQUEST)

            movies = Movie.objects.filter(year__range=(start_year, end_year))
            serializer = MovieSerializers(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
class MoviesWithLessActorsView(APIView):
    def get(self, request):
        movies = Movie.objects.annotate(actor_count=Count('actor')).filter(actor_count__lt=3)
        serializer = MovieSerializers(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommitMovieViewSet(viewsets.ModelViewSet):
    queryset = CommitMovie.objects.all()
    serializer_class = CommitMoviesSerializers

class Login(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, phone_number =serializer.validated_data.get("phone_number"))
        print (user)
        token = get_tokens_for_user(user)
        return Response(data=token, status=status.HTTP_200_OK)

# 1) Telefon yuborish -> OTP generatsiya qilish
class SendOTPView(APIView):
    @swagger_auto_schema(request_body=SentSmsSerializer)
    def post(self, request):
        serializer = SentSmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone_number")
        if not phone:
            return Response({"error": "Telefon raqam kiritilishi kerak"}, status=400)

        otp_obj, created = PhoneOTP.objects.get_or_create(phone_number=phone)
        code = otp_obj.generate_otp()

        # Hozircha terminalga chiqaramiz (SMS API yo‘q)
        print(f"OTP kod: {code}")

        return Response({"message": "OTP yuborildi"}, status=200)


# 2) OTP tekshirish -> user login
class VerifyOTPView(APIView):
    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_obj = serializer.validated_data["otp_obj"]
            phone = serializer.validated_data["phone_number"]

            # OTP tasdiqlash
            otp_obj.is_verified = True
            otp_obj.save()

            return Response({"message": "OTP tasdiqlandi"}, status=200)
        else:
            return Response("error" "Xato kod kiritldi yoki muddati tugagan", status=400)
        
class ChangePasswordApi(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self,request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')
        new_password1 = serializer.validated_data.get('new_password1')
        if new_password1 == new_password:
            user.set_password(new_password)
            user.save()
            return Response({'detail':"Parol uzgartirildi"})
        else:
            return Response({"detail": "Parollar mos emas "}, status=status.HTTP_400_BAD_REQUEST)
