from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
    )

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name="Название",
    )

    description = models.TextField(
        verbose_name="Описание",
    )

    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="catalog/images",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        related_name="products",
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )
    views_counter = models.PositiveIntegerField(
        verbose_name="Количество просмотров",
        default=0,
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name="Пользователь",
                              default=None,  # По умолчанию
                              related_name="products",
                              null=True,
    )

    def __str__(self):
        return (
            f"{self.name} "
            f"{self.description[:30]}..."  # Выводим только начало описания
            f"Категория: {self.category} "
            f"Цена: {self.price} руб."
        )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["create_at", "name", "price"]


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="versions",
        null=True,
        blank=True,
        verbose_name="Версия продукта",
    )
    version_number = models.CharField(max_length=20, verbose_name="Номер версии")
    version_name = models.CharField(max_length=100, verbose_name="Название версии")
    is_active = models.BooleanField(default=False, verbose_name="Активна")

    def __str__(self):
        return f"{self.version_number} {self.version_name}"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["version_number"]
