from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

campos_usuario = list(UserAdmin.fieldsets)
campo = ('Personalização', {'fields': ('observacao',)})
campos_usuario.append(campo)
UserAdmin.fieldsets = tuple(campos_usuario)


admin.site.register(Usuario, UserAdmin)