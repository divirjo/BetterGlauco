# Generated by Django 4.2.13 on 2024-06-28 23:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('investimento', '0012_alter_extratooperacao_operacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extratooperacao',
            name='ativo_perfil_caixa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='operacoes', to='investimento.ativoperfilcaixa', verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='extratooperacao',
            name='custos_transacao',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19, verbose_name='Custos de transação'),
        ),
        migrations.AlterField(
            model_name='extratooperacao',
            name='ir_fonte',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19, verbose_name='Imposto de Renda retido na fonte'),
        ),
        migrations.AlterField(
            model_name='extratooperacao',
            name='operacao',
            field=models.CharField(choices=[('VENDA', 'Venda'), ('COMPRA', 'Compra'), ('SUBSCRIÇÃO', 'Subscrição'), ('DESDOBRO', 'Desdobramento')], max_length=10, verbose_name='Operação'),
        ),
        migrations.AlterField(
            model_name='extratooperacao',
            name='quantidade',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=15, verbose_name='Cotas'),
        ),
        migrations.AlterField(
            model_name='extratooperacao',
            name='valor_unitario',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=19, verbose_name='Valor unitário'),
        ),
        migrations.AlterField(
            model_name='posicaodatabolsa',
            name='ativo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posicoesBolsa', to='investimento.ativo', verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='posicaodatabolsa',
            name='cota_valor',
            field=models.DecimalField(decimal_places=4, default=0, help_text='valor cota na bolsa', max_digits=19, verbose_name='Valor cota (R$)'),
        ),
        migrations.AlterField(
            model_name='posicaodatabolsa',
            name='cota_valor_dolar',
            field=models.DecimalField(decimal_places=4, default=0, help_text='valor em dolar da cota na bolsa             (investimentos internacionais)', max_digits=19, verbose_name='Valor cota (US$)'),
        ),
        migrations.AlterField(
            model_name='posicaodatabolsa',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Data da atualização da cota', verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='posicaodatafundo',
            name='ativo_perfil_caixa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posicoes', to='investimento.ativoperfilcaixa', verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='posicaodatafundo',
            name='cota_sistema_valor',
            field=models.DecimalField(decimal_places=4, default=0, help_text='valor cota do sistema', max_digits=19, verbose_name='Valor cota (R$)'),
        ),
        migrations.AlterField(
            model_name='posicaodatafundo',
            name='cota_valor_dolar',
            field=models.DecimalField(decimal_places=4, default=0, help_text='valor em dolar da cota (investimentos internacionais)', max_digits=19, verbose_name='Valor cota (US$)'),
        ),
        migrations.AlterField(
            model_name='posicaodatafundo',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Data da atualização da cota', verbose_name='Data'),
        ),
    ]