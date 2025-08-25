from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count

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

class ActorAll(APIView):
    def get(self, request):
        actor = Actor.objects.all()
        serializer = ActorSerializers(actor, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ActorCreate(APIView):
    def post(self, request):
        serializer = ActorSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class ActorUpdate(APIView):
    def put(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        serializer = ActorSerializers(actor, data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class ActorDelete(APIView):
    def delete(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        actor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieAll(APIView):
    def get(self, request):
        movie = Movie.objects.all()
        serializer = MovieSerializers(movie, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class MovieCreate(APIView):
    def post(self, request):
        serializer = MovieSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class MovieUpdate(APIView):
    def put(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializers(movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class MovieDelete(APIView):
    def delete(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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