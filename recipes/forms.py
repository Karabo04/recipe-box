from django  import forms
from .models import Recipe, Review


class RecipeForm(forms.ModelForm):
    class Meta:
        model= Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'cooking_time', 'difficulty', 'category', 'image', 'servings']


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model=Review
        fields=[ 'comment', 'rating']
