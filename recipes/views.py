from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users, admin_only
from django.contrib.auth.models import User
from .models import *


def recipe_list(request):
    query=request.GET.get('q')
    recipes=Recipe.objects.all()

    if query:
        recipes= recipes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'recipes/recipes.html', {'recipes': recipes })


def recipe_detail(request, pk):
    recipe= get_object_or_404(Recipe, id=pk)

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe })

