from django.contrib import admin
from .models import Mensagem, Exercicio, FichaTreino, ItemFichaTreino # Importe o novo modelo aqui

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

class ItemFichaTreinoInline(admin.TabularInline):
    model = ItemFichaTreino
    extra = 1

@admin.register(FichaTreino)
class FichaTreinoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'utilizador', 'criada_em')
    inlines = [ItemFichaTreinoInline] # Mostra os exercícios dentro da ficha no admin!

# Registros simples


admin.site.register(ItemFichaTreino)