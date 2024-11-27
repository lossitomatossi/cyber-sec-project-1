from django.contrib import admin

from .models import User, Pet

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'session_token')
    search_fields = ('username',)

class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'owner')
    search_fields = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Pet, PetAdmin)