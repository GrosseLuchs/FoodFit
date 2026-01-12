from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Категория продукта (овощи, мясо, специи и т.д.)"""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название категории"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Allergen(models.Model):
    """Модель аллергена (глютен, лактоза, орехи и т.д.)"""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название аллергена"
    )
    code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Код аллергена",
        help_text="Например: A, B, C или цифровой код"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание аллергена",
        help_text="Какие продукты содержат, симптомы реакции"
    )

    class Meta:
        verbose_name = "Аллерген"
        verbose_name_plural = "Аллергены"
        ordering = ('name',)

    def __str__(self):
        if self.code:
            return f"{self.code} - {self.name}"
        return self.name


class Ingredient(models.Model):
    """Модель для ингредиента (продукта/специи)."""

    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Уникальное название',
        help_text='Официальное или общепринятое название продукта'
    )

    display_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Название для отображения',
        help_text='Короткое название для интерфейса (автозаполнение)'
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    allergen = models.ForeignKey(
        Allergen,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Основной аллерген'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Подробное описание, история, особенности использования'
    )

    calories = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(1000), MinValueValidator(0)],
        verbose_name='Калории',
        help_text='ккал на 100 г продукта'
    )

    protein = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        verbose_name='Белки',
        help_text='г на 100 г продукта'
    )

    fat = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        verbose_name='Жиры',
        help_text='г на 100 г продукта'
    )

    carbohydrates = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        verbose_name='Углеводы',
        help_text='г на 100 г продукта'
    )

    fiber = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        verbose_name='Пищевые волокна',
        help_text='г на 100 г продукта'
    )

    def save(self, *args, **kwargs):
        """Автоматическое заполнение display_name при сохранении"""
        if not self.display_name:
            if len(self.title) > 50:
                self.display_name = self.title[:47] + '...'
            else:
                self.display_name = self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name or self.title

    @property
    def nutrition_summary(self):
        """Сводка по КБЖУ для админки и API"""
        if not self.calories:
            return "Нет данных о пищевой ценности"

        parts = []
        parts.append(f"{self.calories} ккал")
        if self.protein:
            parts.append(f"Б: {self.protein}г")
        if self.fat:
            parts.append(f"Ж: {self.fat}г")
        if self.carbohydrates:
            parts.append(f"У: {self.carbohydrates}г")
        if self.fiber:
            parts.append(f"кл: {self.fiber} г")

        return " | ".join(parts)

    @property
    def has_allergen(self):
        """Проверка наличия аллергена"""
        return self.allergen is not None

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ('title',)
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['category']),
            models.Index(fields=['calories']),
            models.Index(fields=['allergen']),
        ]


class Pairing(models.Model):
    """Модель для сочетания двух ингредиентов."""
    COOKING = 'cook'
    SERVING = 'serve'
    PAIRING_TYPES = [
        (COOKING, 'Для готовки'),
        (SERVING, 'Для подачи')
    ]

    ingredient_a = models.ForeignKey(
        Ingredient,
        related_name='pairings_as_a',
        on_delete=models.CASCADE,
        verbose_name="Первый ингредиент"
    )

    ingredient_b = models.ForeignKey(
        Ingredient,
        related_name='pairings_as_b',
        on_delete=models.CASCADE,
        verbose_name="Второй ингредиент"
    )

    pairing_type = models.CharField(
        max_length=10,
        choices=PAIRING_TYPES,
        default=COOKING,
        verbose_name="Тип сочетания"
    )

    class Meta:
        verbose_name = "Сочетание"
        verbose_name_plural = "Сочетания"
        unique_together = ['ingredient_a', 'ingredient_b', 'pairing_type']

        indexes = [
            models.Index(fields=['ingredient_a', 'pairing_type']),
            models.Index(fields=['ingredient_b', 'pairing_type']),
        ]

    def __str__(self):
        return (f"{self.ingredient_a} вместе с {self.ingredient_b} "
                f"оптимально для {self.get_pairing_type_display()}")

    def clean(self):
        """Валидация перед сохранением"""
        if self.ingredient_a == self.ingredient_b:
            raise ValidationError("Ингредиенты должны быть разными")

        if self.ingredient_a.id and self.ingredient_b.id:
            if self.ingredient_a.id > self.ingredient_b.id:
                self.ingredient_a, self.ingredient_b = (
                    self.ingredient_b,
                    self.ingredient_a
                )

    def save(self, *args, **kwargs):
        """Переопределяем save для автоматической валидации"""
        self.clean()
        super().save(*args, **kwargs)
