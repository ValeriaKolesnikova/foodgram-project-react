from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    username = models.CharField(
        'Уникальный юзернейм',
        max_length=200,
        unique=True,
        blank=False,
        null=False,
        help_text='юзернейм',
        error_messages={'unique': 'юзернейм'},
    )

    first_name = models.CharField(
        'Имя',
        max_length=200,
        blank=False,
        null=False,
        help_text='Имя'
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=200,
        blank=False,
        null=False,
        help_text='Фамилия'
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=200,
        unique=True,
        blank=False,
        null=False,
        help_text='почта'
    )

    password = models.CharField(
        'Пароль',
        max_length=200,
        help_text='Пароль',
        blank=False,
        null=False
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.email}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-author_id',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
