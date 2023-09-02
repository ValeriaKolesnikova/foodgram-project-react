from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from recipes.models import (
    Tag, Recipe, RecipeIngredient,
    Ingredient, FavouriteRecipe, ShoppingCart
)
from users.models import User, Follow
from recipes.validators import validate_ingredients, validate_cooking_time


MIN_INGREDIENT_AMOUNT = 1


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe. Некоторые поля."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Tag."""
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор количества игредиента в рецепте."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient.measurement_unit',
        slug_field='measurement_unit',
        read_only=True,
    )
    name = serializers.SlugRelatedField(
        source='ingredient.name',
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Ingredient."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для всех пользователей."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователей."""
        request = self.context.get('request')
        if request and not request.user.is_anonymous:
            is_subscribed = Follow.objects.filter(
                user=request.user,
                author=obj
            ).exists()
            return is_subscribed
        return False


class RecipeToRepresentationSerializer(serializers.ModelSerializer):
    """Сериализатор для правильного отображения
        после создания/обновления рецепта."""
    class Meta:
        model = Recipe
        fields = (
            'id', 'name',
            'image', 'cooking_time'
        )


class FollowSerializer(UsersSerializer):
    """Сериализатор вывода авторов на которых подписан пользователь."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UsersSerializer.Meta):
        fields = UsersSerializer.Meta.fields + ('recipes', 'recipes_count',)
        read_only_fields = ('email', 'username', 'last_name', 'first_name',)

    def get_recipes(self, obj):
        """Получаем рецепт."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeToRepresentationSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        """Получаем количество рецептов."""
        return Recipe.objects.filter(author=obj).count()


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода списка рецептов."""
    author = UsersSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        """Получаем список ингредиентов для рецепта."""
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('recipeingredient__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        """Находится ли рецепт в избранном."""
        request = self.context.get('request')
        if request and not request.user.is_anonymous:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """Находится ли рецепт в списке покупок."""
        request = self.context.get('request')
        if request and not request.user.is_anonymous:
            return obj.shopping_cart.filter(user=request.user).exists()
        return False


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода количество ингредиентов в рецепте."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class IngredientsEditSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения изменения ингридиентов."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class WriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""
    ingredients = IngredientsEditSerializer(
        many=True,
        required=True,
    )
    tags = PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=True
    )
    image = Base64ImageField(max_length=None)
    author = UsersSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
        )

    def validate(self, data):
        """Проверяем ингредиенты в рецепте."""
        ingredients = data.get('ingredients')
        cooking_time = data.get('cooking_time')
        validate_ingredients(ingredients)
        validate_cooking_time(cooking_time)
        return data

    def create_ingredients(self, ingredients, recipe):
        recipe_ingredients = []

        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
            recipe_ingredients.append(recipe_ingredient)

        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    @atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe, created = Recipe.objects.get_or_create(
            name=validated_data['name'],
            text=validated_data['text'],
            cooking_time=validated_data['cooking_time'],
            defaults=validated_data
        )

        if created:
            recipe.tags.set(tags)
            self.create_ingredients(ingredients, recipe)
        else:
            raise serializers.ValidationError('Рецепт уже существует')

        return recipe

    @atomic
    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            ing = RecipeIngredient.objects.filter(recipe=instance)
            ing.delete()
            self.create_ingredients(ingredients, instance)

        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return ReadRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода рецептов в избранном."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    class Meta:
        model = FavouriteRecipe
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=FavouriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода рецептов в покупках"""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок'
            )
        ]
