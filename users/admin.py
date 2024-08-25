from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'country', 'token',)
    list_filter = ('id', 'email', 'phone', 'country', 'token',)
