# Generated by Django 4.2.8 on 2023-12-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimento', '0007_extratooperacao_ir_fonte_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixa',
            name='ordem_exibicao',
            field=models.IntegerField(default=0),
        ),
    ]
