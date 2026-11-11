from . import views
from django.urls import path
urlpatterns = [
    path('', views.recipe_list, name='recipe_list' ),
    path('recipe_detail/', views.recipe_detail, name='recipe_view')
]

