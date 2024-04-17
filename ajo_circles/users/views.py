from .serializers import UserRegisterationSerializer, CircleCreationSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            #otp = generate_otp()
            if user:
                return Response({"message": "User registered sucessfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class CircleCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CircleCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            circle = serializer.save(creator_id=request.user.id)
            return Response({'id': circle.id, 'message': 'Circle created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberVerificationView():
    pass