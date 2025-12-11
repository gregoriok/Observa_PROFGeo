from django import template
from usuarios.models import Coordenador, Colaborador # Importe seus modelos

register = template.Library()

@register.filter(name='is_coordenador')
def is_coordenador_filter(user):
    """Retorna True se o usuário possuir perfil ativo de Coordenador."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        # Acessa o perfil via related_name
        return user.coordenador_profile.ativo_coordenador
    except Coordenador.DoesNotExist:
        return False