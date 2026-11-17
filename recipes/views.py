from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm, ReviewForm
from .models import Recipe, Review


def registerPage(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        return redirect('login')
    return render(request, 'recipes/register.html')


def loginPage(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('recipe_list')
        messages.error(request, 'Username or password is incorrect.')
    return render(request, 'recipes/login.html')


def logoutUser(request):
    logout(request)
    return redirect('recipe_list')


def recipe_list(request):
    recipes = Recipe.objects.all().annotate(
        average_rating=Avg('review__rating'),
        review_count=Count('review'),
    ).order_by('-date_created')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    max_time = request.GET.get('max_time', '')

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if category:
        recipes = recipes.filter(category=category)
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    if max_time.isdigit():
        recipes = recipes.filter(cooking_time__lte=int(max_time))

    return render(request, 'recipes/recipes.html', {
        'recipes': recipes,
        'categories': Recipe.CATEGORY_CHOICE,
        'difficulties': Recipe.DIFFICULTY_CHOICE,
    })


@login_required(login_url='login')
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    reviews = recipe.review_set.select_related('author').all()
    average_rating = reviews.aggregate(average=Avg('rating'))['average']

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if reviews.filter(author=request.user).exists():
                messages.info(request, 'You already reviewed this recipe.')
                return redirect('recipe_view', pk=pk)
            review = form.save(commit=False)
            review.recipe = recipe
            review.author = request.user
            review.save()
            messages.success(request, 'Review added!')
            return redirect('recipe_view', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form,
    })


@login_required(login_url='login')
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe added!')
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})


@login_required(login_url='login')
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        messages.error(request, 'You can only edit your own recipes.')
        return redirect('recipe_view', pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated!')
            return redirect('recipe_view', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/create_recipe.html', {'form': form, 'editing': True})


@login_required(login_url='login')
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        messages.error(request, 'You can only delete your own recipes.')
        return redirect('recipe_view', pk=pk)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted.')
        return redirect('recipe_list')
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})


@login_required(login_url='login')
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).annotate(
        average_rating=Avg('review__rating'),
        review_count=Count('review'),
    ).order_by('-date_created')
    return render(request, 'recipes/my_recipes.html', {
        'recipes': recipes,
        'categories': Recipe.CATEGORY_CHOICE,
        'difficulties': Recipe.DIFFICULTY_CHOICE,
    })


def about(request):
    return render(request, 'recipes/about.html')
