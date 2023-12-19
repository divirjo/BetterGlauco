from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Ativo, AtivoPerfilCaixa, Caixa, ExtratoOperacao, InstituicaoFinanceira, Parametro, Perfil, PosicaoData, Usuario

campos_usuario = list(UserAdmin.fieldsets)
campo = ('Personalização', {'fields': ('observacao',)})
campos_usuario.append(campo)
UserAdmin.fieldsets = tuple(campos_usuario)

admin.site.register(Parametro)
admin.site.register(Usuario, UserAdmin)

admin.site.register(Perfil)

admin.site.register(Caixa)
admin.site.register(InstituicaoFinanceira)
admin.site.register(Ativo)
admin.site.register(AtivoPerfilCaixa)
admin.site.register(PosicaoData)
admin.site.register(ExtratoOperacao)


