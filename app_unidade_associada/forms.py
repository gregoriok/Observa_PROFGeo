from django import forms
from .models import UnidadeAssociada


class UnidadeAssociadaForm(forms.ModelForm):
    class Meta:
        model = UnidadeAssociada
        fields = [
            'Nome_unidade',
            'Municipio',
            'Estado_UF',
            'Status'
        ]

        widgets = {
            'Nome_unidade': forms.TextInput(attrs={
                # 1. Adiciona a classe CSS (ex: para Bootstrap ou Tailwind)
                'class': 'form-control',
                # 2. Adiciona um placeholder
                'placeholder': 'Digite o nome da unidade'
            }),
            'Municipio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Porto Alegre'
            }),
            'Estado_UF': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: RS'
            }),
            'Status': forms.CheckboxInput(attrs={
                # Opcional: Adicionar classes para Checkbox Input
                'class': 'form-check-input'
            }),
        }