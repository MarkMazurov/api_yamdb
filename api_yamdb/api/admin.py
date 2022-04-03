from django.contrib import admin

from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'birth_year',
        'role',
    )


admin.site.register(CustomUser, UserAdmin)
