from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView


class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'

    def get_login_url(self) -> str:
        return super().get_login_url()


class Ajuda(LoginRequiredMixin, TemplateView):
    template_name = 'ajuda_inicio.html'
    
    
class Valor_compra(LoginRequiredMixin, TemplateView):
    template_name = 'valor_compra.html'
    
    def get_queryset(self):
        ticket = self.request.GET.get('ticket')
        return None
