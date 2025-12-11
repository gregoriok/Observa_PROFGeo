# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Coordenador, Colaborador
from .forms import CadastroUsuarioForm  # Se você quiser usar seu form no Admin

class CoordenadorInline(admin.StackedInline):
    model = Coordenador
    can_delete = False
    verbose_name_plural = 'Perfil de Coordenador'
    fk_name = 'id_usuario'


# Inline para Colaborador
class ColaboradorInline(admin.StackedInline):
    model = Colaborador
    can_delete = False
    verbose_name_plural = 'Perfil de Colaborador'
    fk_name = 'id_usuario'

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    inlines = (CoordenadorInline, ColaboradorInline)

    # Usa seu formulário de criação (opcional)
    add_form = CadastroUsuarioForm

    # Define os campos exibidos no list view
    list_display = ('email', 'nome', 'ativo', 'is_staff', 'is_superuser')
    list_filter = ('ativo', 'is_staff', 'is_superuser')
    # Define os campos para pesquisa e filtros
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'telefone', 'cpf', 'data_cadastro')}),
        ('Permissões', {'fields': ('ativo', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(Coordenador)
admin.site.register(Colaborador)