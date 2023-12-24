from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, UpdateView
from BetterGlauco.funcoes_auxiliares import Funcoes_auxiliares


class InicioAtualizacao(LoginRequiredMixin, TemplateView):
    template_name = 'atualizacao_inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_perfil_selecionado'] = Funcoes_auxiliares.get_perfil_ativo(self.request, **kwargs)
        return context 