from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название блога')
    slug = models.CharField(max_length=200, verbose_name='Ссылка на блог', blank=True)
    content = models.TextField(verbose_name='Контент блога')
    preview = models.ImageField(
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта",
        upload_to="blog_images/",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        blank=True,
        null=True
    )  # Статус блога active/inactive
    count_views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
