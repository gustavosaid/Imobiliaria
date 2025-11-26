from django import forms
from imobiliaria.models import Imovel

class ImovelForms(forms.ModelForm):

    class Meta:
        model = Imovel
        exclude = ['publicada',]
        labels = {

            'categoria': 'Tipo de Imóvel',
            'tamanho' : 'Tamanho (m²)',
            'numero_quarto' : 'Nº de Quartos',
            'valor': 'Valor Locação',
            'bairro': 'Bairro',
            'endereco': 'Endereço',
            'numero': 'Número',
            'descricao': 'Descrição Detalhada',
        }

        widgets = {
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'tamanho':forms.TextInput(attrs={'class':'form-control'}),
            'numero_quarto':forms.TextInput(attrs={'class':'form-control'}),
            'valor':forms.TextInput(attrs={'class':'form-control'}),
            'bairro':forms.TextInput(attrs={'class':'form-control'}),
            'endereco':forms.TextInput(attrs={'class':'form-control'}),
            'numero':forms.TextInput(attrs={'class':'form-control'}),
            'descricao':forms.TextInput(attrs={'class':'form-control'}),
            'foto':forms.FileInput(attrs={'class':'form-control'}),
            
        }
