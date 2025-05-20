from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Avatar, CustomUser, Progress, UserAvatar
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
        profile_image_url = request.user.profile_image_url if hasattr(request.user, 'profile_image_url') else '/media/profile_images/default.png'
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'profile_image': profile_image_url,
            'coins': request.user.coins
        })
    elif request.method == 'POST':
        try:
            avatar_id = request.data.get('avatar_id')
            if avatar_id:
                try:
                    avatar = Avatar.objects.get(id=avatar_id)
                    request.user.profile_image = avatar
                    request.user.save()
                    return JsonResponse({
                        'message': 'Profile image updated successfully',
                        'profile_image': request.user.profile_image_url
                    })
                except Avatar.DoesNotExist:
                    return JsonResponse({'message': 'Avatar not found'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'message': 'No avatar ID provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    data = json.loads(request.body)
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    user = request.user
    
    # Check if old password is correct
    if not user.check_password(old_password):
        return JsonResponse({'message': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Set new password
    user.set_password(new_password)
    user.save()
    
    # Generate new tokens since password change invalidates old ones
    refresh = RefreshToken.for_user(user)
    
    return JsonResponse({
        'message': 'Password changed successfully',
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    return JsonResponse({'message': 'Logged out successfully'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def progress_attempt_view(request):
    if request.method == 'GET':
        try:
            progress = Progress.objects.get(user=request.user)
            return JsonResponse({
                'attempts': progress.attempts,
                'message': 'Successfully retrieved attempts'
            })
        except Progress.DoesNotExist:
            return JsonResponse({
                'attempts': 0,
                'message': 'No progress record found'
            })
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            progress = Progress.objects.get(user=request.user)
            progress.attempts += data.get('attempts', 0)
            progress.save()
            return JsonResponse({
                'attempts': progress.attempts,
                'message': 'Progress attempt updated successfully'
            })
        except Progress.DoesNotExist:
            progress = Progress.objects.create(user=request.user)
            progress.attempts = 1;
            progress.save()
            return JsonResponse({
                'attempts': progress.attempts,
                'message': 'Progress attempt updated successfully'
            })

        except Exception as e:
            return JsonResponse({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard_view(request):
    if request.method == 'GET':
        try:
            users = CustomUser.objects.all()
            
            leaderboard_data = []
            for user in users:
                try:
                    progress = Progress.objects.get(user=user)
                    attempts = progress.attempts
                    coins = progress.coins
                except Progress.DoesNotExist:
                    attempts = 0
                    coins = 0
                
                leaderboard_data.append({
                    'username': user.username,
                    'attempts': attempts,
                    'coins': coins
                })
            
            return JsonResponse({
                'leaderboard': leaderboard_data,
                'message': 'Successfully retrieved leaderboard'
            })
        except Exception as e:
            return JsonResponse({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def progress_coins_view(request):
    if request.method == 'GET':
        try:
            progress = Progress.objects.get(user=request.user)
            return JsonResponse({
                'coins': progress.coins,
                'message': 'Successfully retrieved coins'
            })
        except Progress.DoesNotExist:
            return JsonResponse({
                'coins': 0,
                'message': 'No progress record found'
            })
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            progress = Progress.objects.get(user=request.user)
            progress.coins += data.get('coins', 0)
            progress.save()
            return JsonResponse({
                'coins': progress.coins,
                'message': 'Progress coins updated successfully'
            })
        except Progress.DoesNotExist:
            progress = Progress.objects.create(user=request.user)
            progress.coins = data.get('coins', 0)
            progress.save()
            return JsonResponse({
                'coins': progress.coins,
                'message': 'Progress coins updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def avatar_buy_view(request):
    try:
        data = json.loads(request.body)
        avatar_id = data.get('avatar_id')
        
        if not avatar_id:
            return JsonResponse({
                'message': 'Avatar ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        avatar = Avatar.objects.get(id=avatar_id)
        user = request.user
        
        # Check if user already has this avatar
        if UserAvatar.objects.filter(user=user, avatar=avatar).exists():
            return JsonResponse({
                'message': 'You already own this avatar'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has enough coins
        if user.coins < avatar.price:
            return JsonResponse({
                'message': 'Not enough coins',
                'required': avatar.price,
                'current': user.coins
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Deduct coins and create user-avatar relationship
        user.coins -= avatar.price
        user.profile_image = avatar
        user.save()
        
        # Create record of purchase
        UserAvatar.objects.create(user=user, avatar=avatar)
        
        return JsonResponse({
            'message': 'Avatar bought successfully',
            'remaining_coins': user.coins,
            'profile_image': user.profile_image_url
        })
        
    except Avatar.DoesNotExist:
        return JsonResponse({
            'message': 'Avatar not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def avatar_list_view(request):
    try:
        avatars = Avatar.objects.all()
        avatar_list = []
        
        for avatar in avatars:
            avatar_data = {
                'id': avatar.id,
                'image': avatar.image.url if avatar.image else '/media/avatar_images/default.png',
                'price': avatar.price,
                'is_bought': avatar.user_avatar.filter(user=request.user).exists()
            }
            avatar_list.append(avatar_data)
        
        return JsonResponse({
            'avatars': avatar_list,
            'message': 'Successfully retrieved avatars'
        })
    except Exception as e:
        return JsonResponse({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
