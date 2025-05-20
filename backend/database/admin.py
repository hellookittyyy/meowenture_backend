from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Avatar, Block, Level, Character, Dialog, Progress, Choice, UserAvatar

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'coins')
    search_fields = ('email', 'username')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('profile_image', 'coins')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'default')
    list_editable = ('price', 'default')

class BlockAdmin(admin.ModelAdmin):
    list_display = ('type', 'coordinates', 'size', 'is_start', 'is_finish')
    list_filter = ('type', 'is_start', 'is_finish')

class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_number',)

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DialogAdmin(admin.ModelAdmin):
    list_display = ('character', 'text', 'is_choice', 'stage_number')
    list_filter = ('character', 'is_choice')

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins', 'attempts', 'time_spent', 'total_final_points')
    list_filter = ('user',)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('dialog', 'text', 'final_points', 'level_points')

class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    list_filter = ('user', 'avatar')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Dialog, DialogAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(UserAvatar, UserAvatarAdmin)
