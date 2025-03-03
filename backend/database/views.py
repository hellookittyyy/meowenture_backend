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

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    data = json.loads(request.body)
    email = data.get('email') 
    password = data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_image': user.profile_image_url
            },
        })
    else:
        return JsonResponse({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'profile_image': request.user.profile_image_url
        })
    elif request.method == 'POST':
        try:
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                request.user.profile_image = profile_image
                request.user.save()
                return JsonResponse({
                    'message': 'Profile image updated successfully',
                    'profile_image': request.user.profile_image_url
                })
            return JsonResponse({'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

