from django import forms
from .models import Exercicio
from django.contrib.auth.forms import AuthenticationForm

class ExercicioForm(forms.ModelForm):
    class Meta:
        model = Exercicio
        fields = ['nome', 'grupo_muscular', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-100 focus:border-emerald-500 focus:outline-none transition',
                'placeholder': 'Ex: Supino Reto'
            }),
            'grupo_muscular': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-100 focus:border-emerald-500 focus:outline-none transition'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-100 focus:border-emerald-500 focus:outline-none transition',
                'rows': 3,
                'placeholder': 'Descreva a execução...'
            }),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-100 focus:border-emerald-500 focus:outline-none transition',
        'placeholder': 'Seu usuário'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-100 focus:border-emerald-500 focus:outline-none transition',
        'placeholder': 'Sua senha'
    }))