from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'
    
    def get_login_url(self) -> str:
        return super().get_login_url()

class Ajuda(LoginRequiredMixin, TemplateView):
    template_name = 'ajuda_inicio.html'