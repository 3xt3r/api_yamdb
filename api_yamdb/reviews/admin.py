from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import Category, Genre, Title
from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ['email', 'username', 'role', 'is_active']
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    empty_value_display = '-пусто-'
