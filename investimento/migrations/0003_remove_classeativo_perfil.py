# Generated by Django 4.2.8 on 2023-12-19 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investimento', '0002_alter_ativo_desdobramento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classeativo',
            name='perfil',
        ),
    ]
