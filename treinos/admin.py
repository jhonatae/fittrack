from django.contrib import admin
from .models import Mensagem, Exercicio # Importe o novo modelo aqui

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "criada_em")
    search_fields = ("titulo", "conteudo")

# --- REGISTRO DO EXERCÍCIO NO ADMIN ---
@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ("nome", "grupo_muscular", "criado_em")
    list_filter = ("grupo_muscular",)
    search_fields = ("nome",)