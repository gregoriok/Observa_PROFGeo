from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .decorators import coordenador_required
from .forms import CadastroUsuarioForm, CoordenadorVinculoForm, ColaboradorVinculoForm
from .models import Usuario


class CadastroUsuarioView(CreateView):
    form_class = CadastroUsuarioForm
    template_name = 'usuarios/cadastro.html'
    success_url = reverse_lazy('login')


@staff_member_required  # Apenas usuários staff (Admin) podem acessar
def vincular_cargos_view(request):
    coordenador_form = CoordenadorVinculoForm(prefix='coord')
    colaborador_form = ColaboradorVinculoForm(prefix='colab')

    if request.method == 'POST':
        # Tenta validar o formulário de Coordenador
        if 'salvar_coordenador' in request.POST:
            coordenador_form = CoordenadorVinculoForm(request.POST, prefix='coord')
            if coordenador_form.is_valid():
                coordenador_form.save()
                # Adicione mensagem de sucesso aqui (Django Messages)
                return redirect('vincular_cargos')

        # Tenta validar o formulário de Colaborador
        elif 'salvar_colaborador' in request.POST:
            colaborador_form = ColaboradorVinculoForm(request.POST, prefix='colab')
            if colaborador_form.is_valid():
                colaborador_form.save()
                # Adicione mensagem de sucesso aqui (Django Messages)
                return redirect('vincular_cargos')

    context = {
        'coordenador_form': coordenador_form,
        'colaborador_form': colaborador_form,
        'titulo': 'Vincular Usuários a Cargos'
    }
    return render(request, 'usuarios/vincular_cargos.html', context)


@login_required
def perfil_usuario(request):
    """Exibe o perfil do usuário e atua como dashboard."""
    user = request.user

    # 1. Obter Perfil de Cargo (Opcional, mas útil para mostrar status)
    # Tenta obter o perfil de Coordenador
    try:
        perfil_coordenador = user.coordenador_profile
    except Exception:
        perfil_coordenador = None

    # Tenta obter o perfil de Colaborador
    try:
        perfil_colaborador = user.colaborador_profile
    except Exception:
        perfil_colaborador = None

    context = {
        'perfil_coordenador': perfil_coordenador,
        'perfil_colaborador': perfil_colaborador,
        'titulo': 'Meu Perfil e Dashboard'
    }
    return render(request, 'usuarios/perfil.html', context)


@coordenador_required(redirect_url='perfil')  # Redireciona para o perfil se não for coordenador
def gerenciar_aprovacoes(request):
    user = request.user

    # Apenas superusuários veem TODOS os pendentes. Coordenadores veem apenas os de sua unidade.
    if user.is_superuser:
        pendentes = Usuario.objects.filter(aprovado_coordenador=False)
        unidade_coordenada = None
    else:
        # 1. Encontra a unidade que o Coordenador coordena
        try:
            unidade_coordenada = user.coordenador_profile.id_unidade
        except Exception:
            messages.error(request, "Você não está vinculado a nenhuma unidade para gerenciar aprovações.")
            return redirect('perfil')

        # 2. Filtra usuários que são Colaboradores DAQUELA unidade e não estão aprovados
        pendentes = Usuario.objects.filter(
            aprovado_coordenador=False,
            colaborador_profile__id_unidade=unidade_coordenada
        )

    context = {
        'pendentes': pendentes,
        'unidade': unidade_coordenada,
        'titulo': 'Gerenciar Aprovações de Usuários'
    }
    return render(request, 'usuarios/gerenciar_aprovacoes.html', context)


@coordenador_required(redirect_url='perfil')
def aprovar_usuario(request, user_id):
    usuario_a_aprovar = get_object_or_404(Usuario, pk=user_id)

    # Opcional: Adicionar lógica de segurança para garantir que o Coordenador só aprove
    # usuários da SUA unidade (se não for Superusuário)

    usuario_a_aprovar.aprovado_coordenador = True
    usuario_a_aprovar.ativo = True  # Ativa o usuário globalmente para permitir o login
    usuario_a_aprovar.save()

    messages.success(request, f"O usuário {usuario_a_aprovar.nome} foi aprovado com sucesso e pode fazer login.")
    return redirect('gerenciar_aprovacoes')
