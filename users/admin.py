from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("LiveHelp", {"fields": ("role", "is_online", "avatar")}),
    )
    list_display = ("username", "email", "role", "is_online", "is_staff", "is_superuser")
    list_filter = ("role", "is_online", "is_staff", "is_superuser")
