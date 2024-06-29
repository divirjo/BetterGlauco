from django import forms

from investimento.models import PosicaoDataBolsa, PosicaoDataFundo


class FormPosicaoDataBolsa(forms.ModelForm):
    class Meta:
        model = PosicaoDataBolsa
        fields = '__all__'


class FormNovaPosicaoDataFundo(forms.ModelForm):
    valor_total = forms.DecimalField(
        label='Valor Total (R$)',
        help_text='Valor será dividido pela quantidade de cotas',
    )

    valor_total_dolar = forms.DecimalField(
        initial=0.00,
        label='Valor Total (US$)',
        help_text='Valor será dividido pela quantidade de cotas. Campo \
            opcional',
        required=False,
    )

    class Meta:
        model = PosicaoDataFundo
        fields = '__all__'
        exclude = ('cota_sistema_valor', 'cota_valor_dolar')


class FormEditarPosicaoDataFundo(forms.ModelForm):
    class Meta:
        model = PosicaoDataFundo
        fields = '__all__'
