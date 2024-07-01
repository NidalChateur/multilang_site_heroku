from django.contrib import admin
from django.contrib.auth import get_user_model


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_superuser", "is_staff", "date_joined", "modification_date")


admin.site.register(get_user_model(), UserAdmin)
