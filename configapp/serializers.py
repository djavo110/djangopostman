from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Actor, Movie, CommitMovie
from django.contrib.auth import authenticate


User = get_user_model()

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
        fields = ("id", "title", "movie", "author")
        read_only_fields = ["author"]

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        # Foydalanuvchini tekshirish
        try:
            user = User.objects.get(phone_number=phone_number)
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "success": False,
                "detail": "User does not exist"
            })

        # Parolni tekshirish
        auth_user = authenticate(phone_number=phone_number, password=password)
        if auth_user is None:
            raise serializers.ValidationError({
                "success": False,
                "detail": "Phone_number or password is invalid"
            })

        # Tekshiruvdan o'tgan userni attrs ichiga joylash
        attrs["user"] = auth_user
        return attrs    