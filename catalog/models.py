from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', help_text='Название категории')
    description = models.TextField(verbose_name='Описание', help_text='Описание категории')

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', help_text='Название продукта')
    description = models.TextField(verbose_name='Описание', help_text='Описание продукта')
    preview = models.ImageField(verbose_name='Превью', help_text='Превью продукта', upload_to='products', null=True,
                                blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 help_text='Категория продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', help_text='Цена продукта')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return (f""
                f"{self.name} "
                f"{self.description} "
                f"{self.preview} "
                f"{self.category} "
                f"{self.price} "
                f"{self.create_at} "
                f"{self.update_at}"
                )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

