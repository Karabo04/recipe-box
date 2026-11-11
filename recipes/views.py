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
from .forms import RecipeForm

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")  
        password = request.POST.get("password")
        user= User.objects.create_user( username=username, password=password)
        return redirect('login')
    return render(request, 'recipes/register.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")  
        password = request.POST.get("password")
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return redirect('/')
    return render(request, 'recipes/login.html')


def logoutUser(request):
    logout(request)
    return redirect('recipe_list')

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


login_required(login_url='login')
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('/')
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})

