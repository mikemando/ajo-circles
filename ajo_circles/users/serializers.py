from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'phone_number', 'is_verified', 'bvn', 'credit_score', 'date_joined', 'last_login']
        read_only_fields = ['id', 'bvn', 'date_joined', 'last_login']


class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        return user
    
class OTPVerificationSerielizer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()
