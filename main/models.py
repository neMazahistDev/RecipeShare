from django.db import models
from django.conf import settings


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    category = models.ForeignKey(
        Category, 
        related_name='recipes', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    steps = models.TextField()
    cooking_minutes = models.IntegerField()
    servings = models.IntegerField()
    image = models.ImageField(upload_to='recipes/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('title',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        
    def __str__(self):
        return self.title
    
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')
        ]
        verbose_name = 'Ингредиент с рецептом'
        verbose_name_plural = 'Ингредиенты с рецептами'
        
    def __str__(self):
        return f"{self.ingredient.name} — {self.quantity} {self.unit}"
    
class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        # ordering = ('')
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_user_recipe_favorite')
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        
    def __str__(self):
        return f"{self.user} -> {self.recipe}"
        
class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='comments',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        
    def __str__(self):
        return f"{self.user}: {self.text[:30]}..."