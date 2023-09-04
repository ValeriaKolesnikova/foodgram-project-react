from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientFilter(FilterSet):
    """Фильтр для ингридиентов."""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
        method='filter_by_starting_name'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)

    def filter_by_starting_name(self, queryset, name, value):
        return queryset.filter(Q(name__istartswith=value))


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
