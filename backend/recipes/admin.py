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


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name', 'color',)
    search_fields = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'get_ingredients',
        'get_tags',
        'in_favorites',
    )
    search_fields = ('author__username', 'name', 'tags__name',)
    list_filter = ('author', 'name', 'tags',)

    def get_ingredients(self, object):
        return ',\n'.join(
            ingredient.name for ingredient in object.ingredients.all()
        )

    get_ingredients.short_description = 'Ингредиенты'

    def get_tags(self, object):
        return '\n'.join(tag.name for tag in object.tags.all())

    get_tags.short_description = 'Теги'

    def in_favorites(self, obj):
        return FavouriteRecipe.objects.filter(recipe=obj).count()

    in_favorites.short_description = 'Добавлен в избранное'

    inlines = (RecipeIngredientInline,)


@admin.register(FavouriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('user__username', 'recipe__name', )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('user__username', 'recipe__name', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'author',
    )
    list_filter = ('user',)
    search_fields = ('user__username', )
    empty_value_display = '-пусто-'
