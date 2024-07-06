# Generated by Django 4.2.8 on 2023-12-19 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativo',
            name='desdobramento',
            field=models.DecimalField(decimal_places=10, default=0, help_text='Quanto representa a cota brasileira em relação ao ativo original (somente BDRs)', max_digits=15),
        ),
        migrations.AlterField(
            model_name='ativo',
            name='ticket_original',
            field=models.CharField(blank=True, default='', help_text='Código de negociação original do ativo (somente BDRs)', max_length=10),
        ),
    ]
