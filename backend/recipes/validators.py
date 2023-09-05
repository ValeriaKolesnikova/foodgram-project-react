from django.core.exceptions import ValidationError
from rest_framework import serializers

MIN_AMOUNT = 1


def validate_ingredients(ingredients):
    ingredients_data = [ingredient.get('id') for ingredient in ingredients]
    if len(ingredients_data) != len(set(ingredients_data)):
        raise serializers.ValidationError(
            'Ингредиенты рецепта должны быть уникальными'
        )
    if not ingredients:
        raise serializers.ValidationError(
            'Рецепт не может быть без ингредиентов'
        )
    for ingredient in ingredients:
        amount = int(ingredient.get('amount'))
        if amount < MIN_AMOUNT:
            raise serializers.ValidationError(
                f'Некорректное количество ингредиента. '
                f'Количество должно быть больше {MIN_AMOUNT}.'
            )
    return ingredients


def validate_cooking_time(value):
    if not value or int(value) < MIN_AMOUNT:
        raise ValidationError(
            f'Некорректное время готовки. '
            f'Время должно быть больше {MIN_AMOUNT} минуты.'
        )
