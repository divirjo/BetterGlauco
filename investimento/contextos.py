from .models import Perfil


def lista_perfis_usuario(request):
    usuario_ativo_id = request.user.id
    lista_perfis_autorizados = Perfil.objects.filter(
        usuarios_permitidos=usuario_ativo_id
    ).order_by('nome')
    return {'lista_perfis': lista_perfis_autorizados}
