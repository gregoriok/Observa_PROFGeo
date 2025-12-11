from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Cadastro de Usuário
    path('cadastro', views.CadastroUsuarioView.as_view(), name='cadastro'),

    # Login e Logout (geralmente usamos as views nativas do Django)
    path('login', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('cargos/vincular/', views.vincular_cargos_view, name='vincular_cargos'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('aprovacoes/', views.gerenciar_aprovacoes, name='gerenciar_aprovacoes'),
    path('aprovacoes/aprovar/<uuid:user_id>/', views.aprovar_usuario, name='aprovar_usuario'),
]