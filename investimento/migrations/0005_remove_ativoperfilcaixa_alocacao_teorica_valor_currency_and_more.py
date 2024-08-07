# Generated by Django 4.2.8 on 2023-12-21 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimento', '0004_remove_ativoperfilcaixa_caixa_alocacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ativoperfilcaixa',
            name='alocacao_teorica_valor_currency',
        ),
        migrations.RemoveField(
            model_name='extratooperacao',
            name='custos_transacao_currency',
        ),
        migrations.RemoveField(
            model_name='extratooperacao',
            name='valor_unitario_currency',
        ),
        migrations.RemoveField(
            model_name='posicaodata',
            name='cota_sistema_valor_currency',
        ),
        migrations.RemoveField(
            model_name='posicaodata',
            name='dividendos_currency',
        ),
        migrations.AlterField(
            model_name='ativoperfilcaixa',
            name='alocacao_teorica_valor',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='extratooperacao',
            name='custos_transacao',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='extratooperacao',
            name='valor_unitario',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='posicaodata',
            name='cota_sistema_valor',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='posicaodata',
            name='dividendos',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19),
        ),
    ]
