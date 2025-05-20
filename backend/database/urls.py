from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('progress/attempt/', views.progress_attempt_view, name='progress_attempt'),
    path('progress/coins/', views.progress_coins_view, name='progress_coins'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('avatar/buy/', views.avatar_buy_view, name='avatar_buy'),
    path('avatar/list/', views.avatar_list_view, name='avatar_list'),
    path('avatar/buy/<int:avatar_id>/', views.avatar_buy_view, name='avatar_buy'),
]