from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'
