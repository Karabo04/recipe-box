from . import views
from django.urls import path
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('create/', views.create_recipe, name='create_recipe'),

    path('', views.recipe_list, name='recipe_list' ),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_view'),
    path('create/', views.create_recipe, name='create_recipe'),
]

