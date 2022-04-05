from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


admin.site.register(CustomUser, UserAdmin)
