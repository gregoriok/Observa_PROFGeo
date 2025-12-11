from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_unidade_associada, name='unidade_list'),
    path('adicionar/', views.create_unidade_associada, name='unidade_create'),
    path('<uuid:pk>/editar/', views.update_unidade_associada, name='unidade_update'),

    # (Opcional)
    # path('<uuid:pk>/excluir/', views.unidade_delete, name='unidade_delete'),
]