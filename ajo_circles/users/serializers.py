from rest_framework import serializers
from .models import User, Circle
from decimal import Decimal, InvalidOperation

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
    
class OTPVerificationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

class CircleCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = '__all__'
    
    def validate_number_of_participants(self, value):
        participants_no = value.strip()

        try:
            value = int(participants_no)
            if value <= 0:
                raise serializers.ValidationError('Number of participants must be greater than zero')
        except ValueError:
            raise serializers.ValidationError('Number of participants must be a valid integer')
        
        return value
    
    def validate_goal_amount(self, value):
        goal_amount = value.strip()

        try:
            goal_amount = Decimal(goal_amount)
            if goal_amount < 60000.00:
                raise serializers.ValidationError('You can only create circles with payout up to 60000 Naira')
        except InvalidOperation:
            raise serializers.ValidationError('Goal amount must be a valid decimal')
       
        return goal_amount
    
    def validate_circle_image(self, value):
        if not value.content_type.startswith('image'):
            raise serializers.ValidationError('File is not an image')
        return value

    def create(self, validated_data):
        image = validated_data.pop('image')

        circle = Circle.objects.create(**validated_data)
        circle.circle_image = image
        circle.save()

        return circle


