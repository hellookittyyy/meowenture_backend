from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create new user
    user = CustomUser.objects.create_user(username=username, email=email, password=password)
    user.save()
    
    return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)