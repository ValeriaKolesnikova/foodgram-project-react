from django.contrib import admin

from recipes.models import (
    Tag, Recipe, Ingredient,
    RecipeIngredient, FavouriteRecipe,
    ShoppingCart
)
from users.models import Follow


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name', 'color',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'in_favorites', )
    list_filter = ('name', 'author', 'tags', )
    search_fields = ('name', 'author__username', 'tags__name',)
    empty_value_display = '-пусто-'

    def in_favorites(self, obj):
        return FavouriteRecipe.objects.filter(recipe=obj).count()

    in_favorites.short_description = 'Добавлен в избранное'
    inlines = (RecipeIngredientInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(FavouriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('user', 'recipe', )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('user', 'recipe', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'author',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
