from rest_framework import serializers
from .models import *

class ActorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("name", "year", "genre", "actor")

class CommitMoviesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommitMovie
    fields = ("title", "movie", "author")