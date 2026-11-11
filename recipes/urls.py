from . import views
from django.urls import path
urlpatterns = [
    path('', views.recipe_list, name='recipe_list' ),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_view')
]

