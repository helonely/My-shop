# Generated by Django 5.0.6 on 2024-07-22 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_blog_count_views_blog_create_at_blog_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="is_active",
            field=models.BooleanField(
                blank=True, default=True, null=True, verbose_name="Активен"
            ),
        ),
    ]
