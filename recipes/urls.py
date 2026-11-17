from django.urls import path

from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('about/', views.about, name='about'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_view'),
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
]
