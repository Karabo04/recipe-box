from django  import forms
from .models import Recipe, Review


class RecipeForm(forms.ModelForm):
    class Meta:
        model= Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'cooking_time', 'difficulty', 'category', 'image', 'servings']


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['reviewer_name', 'comment', 'rating']