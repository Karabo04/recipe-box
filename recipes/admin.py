from django.contrib import admin
from .models import *


class RecipeAdmin(admin.ModelAdmin):
    list_display=['title', 'category', 'difficulty', 'cooking_time', 'author', 'date_created']
    list_filter=['category', 'difficulty']
    search_fields=['title']
admin.site.register(Recipe, RecipeAdmin)