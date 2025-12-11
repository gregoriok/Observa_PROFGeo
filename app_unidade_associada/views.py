from django.shortcuts import render, redirect, get_object_or_404

from app_unidade_associada.forms import UnidadeAssociadaForm
from app_unidade_associada.models import UnidadeAssociada
import datetime


def view_unidade_associada(request):
    """Lista todas as unidades e exibe os botões '+' e 'Lápis'."""
    unidades = UnidadeAssociada.objects.all().order_by('Nome_unidade')  # Ordena para melhor UX

    context = {
        'unidades': unidades,
    }
    return render(request, 'unidade_list.html', context)

def create_unidade_associada(request):
    """Lida com a criação de uma nova unidade."""
    if request.method == 'POST':
        form = UnidadeAssociadaForm(request.POST)
        if form.is_valid():
            unidade = form.save(commit=False)
            unidade.Data_insercao = datetime.date.today()
            unidade.save()

            return redirect('unidade_list')
    else:
        # GET: Exibe o formulário vazio
        form = UnidadeAssociadaForm()

    context = {
        'form': form,
        'titulo': 'Adicionar Nova Unidade Associada'
    }
    return render(request, 'unidade_form.html', context)  # Reutiliza um template de formulário


def update_unidade_associada(request, pk):
    """Lida com a edição de uma unidade existente."""
    # Garante que a unidade exista, senão retorna erro 404
    unidade = get_object_or_404(UnidadeAssociada, pk=pk)

    if request.method == 'POST':
        # Instancia o formulário, preenchendo-o com os dados do POST e a instância atual
        form = UnidadeAssociadaForm(request.POST, instance=unidade)
        if form.is_valid():
            form.save()  # Salva as alterações na instância existente
            return redirect('unidade_list')
    else:
        # GET: Exibe o formulário pré-preenchido com os dados da unidade
        form = UnidadeAssociadaForm(instance=unidade)

    context = {
        'form': form,
        'titulo': f'Editar Unidade: {unidade.Nome_unidade}'
    }
    return render(request, 'unidade_form.html', context)  # Reutiliza o template