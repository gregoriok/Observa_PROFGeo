# usuarios/forms.py
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from app_unidade_associada.models import UnidadeAssociada
from .models import Usuario, Colaborador, Coordenador


class CadastroUsuarioForm(UserCreationForm):
    # Campos que não estão no AbstractBaseUser (mas estão no modelo Usuario)
    telefone = forms.CharField(max_length=15, required=False)
    cpf = forms.CharField(max_length=14, required=False, label="CPF")
    id_unidade = forms.ModelChoiceField(
        queryset=UnidadeAssociada.objects.all(),
        label="Unidade Associada de Trabalho"
    )
    area_atuacao = forms.CharField(max_length=100, label="Área de Atuação")
    ano_ingresso = forms.IntegerField(label="Ano de Ingresso na Unidade")
    # Sobrescreve o Meta para usar modelo de Usuário
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('nome', 'email', 'telefone', 'cpf','id_unidade', 'area_atuacao', 'ano_ingresso')  # Campos a serem exibidos no formulário

    # Sobrescreve o método save para garantir que a senha seja hasheada
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        user.ativo = False
        user.aprovado_coordenador = False
        if commit:
            user.save()
            unidade = self.cleaned_data.get('id_unidade')
            atuacao = self.cleaned_data.get('area_atuacao')
            ingresso = self.cleaned_data.get('ano_ingresso')
            Colaborador.objects.create(
                id_usuario=user,
                id_unidade=unidade,
                area_atuacao=atuacao,
                ano_ingresso=ingresso,

                ativo_colaborador=False,
                ano_referencia=date.today().year
            )
        return user


class CoordenadorVinculoForm(forms.ModelForm):
    # Campo para selecionar o usuário (PK/FK)
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_superuser=False),  # Exclui superusuários
        label="Vincular Usuário"
    )

    class Meta:
        model = Coordenador
        # Excluímos id_usuario porque ele será preenchido pelo campo 'usuario'
        fields = ('usuario', 'formacao', 'id_unidade', 'ano_vigencia', 'ativo_coordenador')
        # Note que 'id_unidade' é o nome do campo FK no modelo

    def save(self, commit=True):
        usuario = self.cleaned_data.get('usuario')

        # O campo PK/FK (id_usuario) será o usuário selecionado
        self.instance.id_usuario = usuario

        # Verifica se o perfil já existe (para evitar erro de PK duplicada)
        if Coordenador.objects.filter(id_usuario=usuario).exists():
            raise ValidationError("Este usuário já possui um perfil de coordenador.")

        return super().save(commit)


class ColaboradorVinculoForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_superuser=False),
        label="Vincular Usuário"
    )

    class Meta:
        model = Colaborador
        fields = ('usuario', 'area_atuacao', 'ano_ingresso', 'ano_referencia', 'id_unidade', 'ativo_colaborador')

    def save(self, commit=True):
        self.instance.id_usuario = self.cleaned_data.get('usuario')
        if Colaborador.objects.filter(id_usuario=self.instance.id_usuario).exists():
            raise ValidationError("Este usuário já possui um perfil de colaborador.")
        return super().save(commit)