from django.contrib import admin

from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


admin.site.register(CustomUser, UserAdmin)
