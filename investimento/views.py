from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from .brd import BRD


class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'

    def get_login_url(self) -> str:
        return super().get_login_url()


class Ajuda(LoginRequiredMixin, TemplateView):
    template_name = 'ajuda_inicio.html'
    
    
class Valor_compra(LoginRequiredMixin, TemplateView):
    template_name = 'valor_compra.html'
    calculo_brd = {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brd_ativo = BRD(self.request)
        self.calculo_brd['Ticket'] = brd_ativo.ativo_selecionado.ticket
        if brd_ativo.ativo_selecionado.ticket:
            self.calculo_brd['USA'] = brd_ativo.ativo_selecionado.ticket_original
            self.calculo_brd['Desdobramento'] = int(brd_ativo.ativo_selecionado.desdobramento)
            self.calculo_brd['Dolar'] = brd_ativo.dolar_compra
        context['calculo_brd'] = self.calculo_brd
        return context
    
        