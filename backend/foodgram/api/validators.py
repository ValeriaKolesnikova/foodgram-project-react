from rest_framework import serializers

MIN_INGREDIENT_AMOUNT = 1

def validate_ingredients(ingredients):
    if not ingredients:
        raise serializers.ValidationError(
            'Рецепт не может быть без ингредиентов'
        )
    for ingredient in ingredients:
        amount = int(ingredient.get('amount'))
        if amount < MIN_INGREDIENT_AMOUNT:
            raise serializers.ValidationError(
                f'Некорректное количество ингредиента. '
                f'Количество должно быть больше {MIN_INGREDIENT_AMOUNT}.'
            )
    return ingredients
