# Generated by Django 4.1 on 2025-06-13 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_alter_author_patronymic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='books',
        ),
    ]
