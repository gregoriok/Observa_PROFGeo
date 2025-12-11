from django.urls import path
from . import views

urlpatterns = [
    # 1. TELA DE VISUALIZAÇÃO/LISTAGEM (READ) - URL principal
    path('', views.view_unidade_associada, name='unidade_list'),

    # 2. TELA DE INSERÇÃO (CREATE) - Redirecionada pelo botão '+'
    path('adicionar/', views.create_unidade_associada, name='unidade_create'),

    # 3. TELA DE EDIÇÃO (UPDATE) - Acessada pelo botão de Lápis
    # O <uuid:pk> captura o ID único (PK) da unidade que será editada.
    path('<uuid:pk>/editar/', views.update_unidade_associada, name='unidade_update'),

    # (Opcional, mas útil) TELA DE EXCLUSÃO (DELETE)
    # path('<uuid:pk>/excluir/', views.unidade_delete, name='unidade_delete'),
]