from django.db import models
from django.contrib.auth.models import User

class Mensagem(models.Model):
    titulo = models.CharField(max_length=120)
    conteudo = models.TextField()
    autor = models.CharField(max_length=80, default="Jhonata")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return self.titulo

# --- NOVO MODELO PARA O FITTRACK ---
class Exercicio(models.Model):
    GRUPOS_MUSCULARES = [
        ('PEITO', 'Peitoral'),
        ('COSTAS', 'Costas'),
        ('PERNAS', 'Membros Inferiores'),
        ('BRACOS', 'Braços/Ombros'),
        ('CORE', 'Abdominais/Core'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercicios", verbose_name="Usuário")

    nome = models.CharField(max_length=100, verbose_name="Nome do Exercício")
    grupo_muscular = models.CharField(max_length=10, choices=GRUPOS_MUSCULARES, verbose_name="Grupo Muscular")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição da Execução")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Exercício"
        verbose_name_plural = "Exercícios"

    def __str__(self):
        return f"{self.nome} ({self.get_grupo_muscular_display()})"