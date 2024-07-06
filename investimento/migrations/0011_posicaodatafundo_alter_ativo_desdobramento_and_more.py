# Generated by Django 4.2.8 on 2024-02-12 10:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('investimento', '0010_remove_posicaodata_dividendos_ativo_dividendos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosicaoDataFundo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('cota_sistema_valor', models.DecimalField(decimal_places=4, default=0, help_text='valor cota do sistema', max_digits=19)),
                ('cota_valor_dolar', models.DecimalField(decimal_places=4, default=0, help_text='valor em dolar da cota (investimentos internacionais)', max_digits=19)),
            ],
        ),
        migrations.AlterField(
            model_name='ativo',
            name='desdobramento',
            field=models.DecimalField(decimal_places=10, default=0, help_text='Quanto representa a cota brasileira em relação ao ativo             original (somente BDRs)', max_digits=15),
        ),
        migrations.AlterField(
            model_name='ativoperfilcaixa',
            name='aloc_teor_percent_caixa',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Percentual ideal de alocação do ativo             em referência ao valor alocando na caixa', max_digits=5),
        ),
        migrations.AlterField(
            model_name='ativoperfilcaixa',
            name='aloc_teor_percent_carteira',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Percentual ideal de alocação do ativo             em referência ao total investido', max_digits=5),
        ),
        migrations.AlterField(
            model_name='ativoperfilcaixa',
            name='alocacao_teorica_valor',
            field=models.DecimalField(decimal_places=4, default=0, help_text='Valor ideal de alocação no ativo', max_digits=19),
        ),
        migrations.AlterField(
            model_name='posicaodatabolsa',
            name='cota_valor_dolar',
            field=models.DecimalField(decimal_places=4, default=0, help_text='valor em dolar da cota na bolsa             (investimentos internacionais)', max_digits=19),
        ),
        migrations.DeleteModel(
            name='PosicaoData',
        ),
        migrations.AddField(
            model_name='posicaodatafundo',
            name='ativo_perfil_caixa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posicoes', to='investimento.ativoperfilcaixa'),
        ),
    ]