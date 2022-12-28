from django.views.generic import TemplateView

class Homepage(TemplateView):
    template_name = 'index.html'
    
class Sobre(TemplateView):
    template_name = 'sobre.html'
    
class Contato(TemplateView):
    template_name = 'contato.html'