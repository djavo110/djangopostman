from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Actor, Movie, CommitMovie, PhoneOTP
from django.contrib.auth import authenticate


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ( 'phone_number', 'email', 'password', 'is_admin', 'is_staff', 'is_student')
        read_only_fields = ['is_active', 'is_teacher']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

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
    
class SentSmsSerializer(serializers.Serializer):
        phone_number = serializers.CharField()        

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data.get("phone_number")
        otp = data.get("otp")

        try:
            otp_obj = PhoneOTP.objects.get(phone_number=phone)
        except PhoneOTP.DoesNotExist:
            raise serializers.ValidationError({"phone_number": "Bunday telefon raqam topilmadi"})

        if otp_obj.otp != otp or not otp_obj.is_valid():
            raise serializers.ValidationError({"otp": "OTP noto'g'ri yoki muddati tugagan"})

        # Agar hammasi to‘g‘ri bo‘lsa, otp obyektni serializer ichida saqlaymiz
        data["otp_obj"] = otp_obj
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=6)
    new_password1 = serializers.CharField(required=True, min_length=6)
