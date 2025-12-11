from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def is_coordenador(user):
    """
    Verifica se o usuário está ativo e possui um perfil de Coordenador ativo.
    """
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    try:
        return user.coordenador_profile.ativo_coordenador
    except Exception:
        return False


def coordenador_required(function=None, redirect_url='home'):
    """
    Decorator que só permite acesso se o usuário for Coordenador ativo.
    """
    actual_decorator = user_passes_test(
        is_coordenador,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator