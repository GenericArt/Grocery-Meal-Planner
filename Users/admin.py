from django.contrib import admin
from Users.models import UserAuth


@admin.register(UserAuth)
class UserAdmin(admin.ModelAdmin):
    pass