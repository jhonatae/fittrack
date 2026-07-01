from django import forms

from .models import Mensagem

# Classe Tailwind reaproveitada por todos os campos do formulário.
INPUT = (
    "w-full rounded-lg bg-slate-800 border border-white/10 px-3 py-2 "
    "text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-400"
)


class MensagemForm(forms.ModelForm):
    # Campo extra (não existe no model): o visitante digita as tags como texto
    # livre separado por vírgula. Vamos transformá-lo em objetos Tag na view.
    tags = forms.CharField(
        required=False,
        label="Tags",
        help_text="Separe por vírgula. Ex.: django, tutorial, iniciante",
        widget=forms.TextInput(attrs={"class": INPUT}),
    )

    class Meta:
        model = Mensagem
        fields = ["titulo", "conteudo", "autor", "categoria"]
        labels = {
            "titulo": "Título",
            "conteudo": "Conteúdo",
            "autor": "Autor",
            "categoria": "Categoria",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"class": INPUT}),
            "conteudo": forms.Textarea(attrs={"class": INPUT, "rows": 4}),
            "autor": forms.TextInput(attrs={"class": INPUT}),
            "categoria": forms.Select(attrs={"class": INPUT}),
        }