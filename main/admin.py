from django.contrib import admin
from .models import Category, Recipe, Ingredient, RecipeIngredient, Favorite, Comment

# --- 1. Категории ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created')
    list_filter = ('created',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} 


# --- 2. Ингредиенты ---
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'update')
    search_fields = ('name',)
    list_filter = ('created',)


# --- 3. Встроенные ингредиенты для рецепта (Inline) ---
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ('ingredient',)


# --- 4. Рецепты ---
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'cooking_minutes', 'servings', 'created')
    list_editable = ('category', 'cooking_minutes', 'servings')
    list_filter = ('category', 'user', 'created')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    inlines = [RecipeIngredientInline]
    # Для выбора пользователя используем поиск (если пользователей много), а не выпадающий список
    raw_id_fields = ('user',)


# --- 5. Ингредиенты в рецептах (Промежуточная таблица) ---
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity', 'unit')
    list_filter = ('unit', 'ingredient')
    search_fields = ('recipe__title', 'ingredient__name')
    list_editable = ('quantity', 'unit')


# --- 6. Избранное ---
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created')
    list_filter = ('created', 'user')
    search_fields = ('user__username', 'recipe__title')
    # Используем raw_id_fields, чтобы не грузить тысячи записей в выпадающий список
    raw_id_fields = ('user', 'recipe')


# --- 7. Комментарии ---
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'short_text', 'created')
    list_filter = ('created', 'user')
    search_fields = ('text', 'user__username', 'recipe__title')
    raw_id_fields = ('user', 'recipe')

    # Кастомная колонка для обрезки длинного текста
    @admin.display(description='Текст комментария')
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text