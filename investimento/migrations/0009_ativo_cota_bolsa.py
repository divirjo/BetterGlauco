# Generated by Django 4.2.8 on 2024-01-25 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimento', '0008_caixa_ordem_exibicao'),
    ]

    operations = [
        migrations.AddField(
            model_name='ativo',
            name='cota_bolsa',
            field=models.BooleanField(default=False, help_text='O ativo possui cota na bolsa?'),
        ),
    ]