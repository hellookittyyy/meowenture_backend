from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ForeignKey('Avatar', on_delete=models.SET_NULL, null=True, related_name='users')
    coins = models.IntegerField(default=99)

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    @property
    def profile_image_url(self):
        if self.profile_image and self.profile_image.image:
            return self.profile_image.image.url
        return '/media/profile_images/avatar_1.png'

    def save(self, *args, **kwargs):
        if not self.profile_image:
            default_avatar = Avatar.objects.filter(default=True).first()
            if default_avatar:
                self.profile_image = default_avatar
            else:
                first_avatar = Avatar.objects.first()
                if first_avatar:
                    self.profile_image = first_avatar
        super().save(*args, **kwargs)
    
class Choice(models.Model):
    dialog = models.ForeignKey('Dialog', on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    next_dialog = models.ForeignKey('Dialog', on_delete=models.CASCADE, related_name='next_dialogues')
    final_points = models.IntegerField(default=0)
    level_points = models.IntegerField(default=0)

class Block(models.Model):
    type = models.CharField(max_length=255, choices=[('platform', 'Platform'), ('obstacle', 'Obstacle'), ('background obj', 'Background obj'), ('item', 'Item'), ('enemy', 'Enemy')], default='platform')
    coordinates = models.CharField(max_length=255, default='0,0')
    size = models.CharField(max_length=255, default='1,1')
    image = models.ImageField(upload_to='block_images/', default ='block_images/default.png')
    is_start = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)

class Level(models.Model):
    background = models.ImageField(upload_to='level_backgrounds/', default='level_backgrounds/default.png')
    level_number = models.IntegerField()
    block = models.ManyToManyField(Block)
    next_dialog = models.ForeignKey('Dialog', on_delete=models.CASCADE, related_name='next_dialogs', default='1')

class Character(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='character_images/', default ='character_images/default.png')

class Dialog(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='dialogs')
    next_dialog = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='next_dialoges')
    next_level = models.ForeignKey('Level', on_delete=models.CASCADE, related_name='dialogs', null=True)
    text = models.TextField()
    is_choice = models.BooleanField(default=False)
    stage_number = models.IntegerField(default=1)
    background = models.ImageField(upload_to='dialog_backgrounds/', default='dialog_backgrounds/default.png')

class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progress')
    # level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='progress', null=True)
    coins = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)
    total_final_points = models.IntegerField(default=0)
    is_level = models.BooleanField(default=False)
    current_phase = models.IntegerField(default=1)

class Avatar(models.Model):
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    price = models.IntegerField(default=0)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'profile_images/default.png'
        super().save(*args, **kwargs)

    @property
    def url(self):
        return self.image.url if self.image else '/media/profile_images/default.png'

class UserAvatar(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_avatar')
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, related_name='user_avatar')


# class OTP(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField()

#     def __str__(self):
#         return f"OTP for {self.user.email}"