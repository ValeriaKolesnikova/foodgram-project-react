from django.db import models
from django.db.models import UniqueConstraint

from users.models import User

FIELD_MAX_LENGTH = 200
COLOR_MAX_LENGHT = 7 

class Tag(models.Model):
    name = models.CharField(
        max_length=FIELD_MAX_LENGTH,
        verbose_name='Название тега',
        unique=True,
    )
    color = models.CharField(
        max_length=COLOR_MAX_LENGHT,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=FIELD_MAX_LENGTH,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    text = models.TextField('Описание')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipe'
    )
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        'Ingredient', through='RecipeIngredient'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
        null=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=FIELD_MAX_LENGTH,
        verbose_name=('Название ингредиента'),
    )
    measurement_unit = models.CharField(
        max_length=FIELD_MAX_LENGTH,
        verbose_name=('Единица измерения'),
    )

    class Meta:
        verbose_name = ('Ингредиент')
        verbose_name_plural = ('Ингредиенты')
        ordering = ('name',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favourite')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
