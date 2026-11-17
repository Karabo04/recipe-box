from django.db import models
from django.contrib.auth.models import User
class Recipe(models.Model):
    DIFFICULTY_CHOICE=[
        ('easy', 'Easy' ),
        ('medium', 'Medium' ),
        ('hard', 'Hard' ),
    ]
    CATEGORY_CHOICE=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
        ('snack', 'Snack')
    ]
    title= models.CharField(max_length=50, blank=False)
    description=models.TextField()
    ingredients=models.TextField( blank=False)
    instructions=models.TextField(blank=False)
    cooking_time=models.IntegerField()
    servings= models.IntegerField()
    difficulty=models.CharField(max_length=10, choices=DIFFICULTY_CHOICE)
    category= models.CharField(max_length=10, choices=CATEGORY_CHOICE)
    image= models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    date_created=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    recipe= models.ForeignKey(Recipe, on_delete= models.CASCADE)    
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.TextField()
    rating= models.IntegerField()
    date_created= models.DateField(auto_now_add=True)

    class Meta:
        unique_together=['recipe', 'author']

    def __str__(self):
        return f'{self.author.username}: {self.recipe.title}'
