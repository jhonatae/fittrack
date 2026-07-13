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
    

class PerfilUtilizador(models.Model):
    utilizador = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    peso = models.FloatField(verbose_name="Peso (kg)", default=70.0)
    altura = models.FloatField(verbose_name="Altura (m)", default=1.70)
    objetivo = models.CharField(max_length=100, verbose_name="Objetivo de Treino", default="Manutenção")
    atualizado_em = models.DateTimeField(auto_now=True)

    # Cálculo dinâmico do Índice de Massa Corporal (IMC) na camada de domínio
    def imc(self):
        if self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return 0

    class Meta:
        verbose_name = "Status de Utilizador"
        verbose_name_plural = "Status de Utilizadores"

    def __str__(self):
        return f"Status de {self.utilizador.username}"


# --- ISSUE #15: MODELO DE TREINO AGRUPADOR (FICHA) ---
class FichaTreino(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fichas")
    nome = models.CharField(max_length=100, verbose_name="Nome da Ficha")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição/Observações")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em"]
        verbose_name = "Ficha de Treino"
        verbose_name_plural = "Fichas de Treino"

    def __str__(self):
        return self.nome


# --- RELACIONAMENTO MUITOS-PARA-MUITOS ATRIBUÍDO COM CARGA E SÉRIES ---
class ItemFichaTreino(models.Model):
    ficha = models.ForeignKey(FichaTreino, on_delete=models.CASCADE, related_name="itens")
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    series = models.PositiveIntegerField(default=3, verbose_name="Séries")
    repeticoes = models.CharField(max_length=50, default="10", verbose_name="Repetições")
    carga = models.PositiveIntegerField(default=0, verbose_name="Carga (kg)")

    class Meta:
        verbose_name = "Exercício da Ficha"
        verbose_name_plural = "Exercícios da Ficha"

    def __str__(self):
        return f"{self.exercicio.nome} -> {self.ficha.nome}"


# --- ISSUE #14: HISTÓRICO DE UTILIZADOR ---
class HistoricoTreino(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="historicos")
    ficha = models.ForeignKey(FichaTreino, on_delete=models.SET_NULL, null=True, blank=True)
    nome_ficha_backup = models.CharField(max_length=100, blank=True, null=True) # Mantém histórico mesmo se a ficha for eliminada
    realizado_em = models.DateTimeField(auto_now_add=True)
    duracao_minutos = models.PositiveIntegerField(default=45, verbose_name="Duração (minutos)")
    comentarios = models.TextField(blank=True, null=True, verbose_name="Notas de Execução")

    class Meta:
        ordering = ["-realizado_em"]
        verbose_name = "Histórico de Treino"
        verbose_name_plural = "Históricos de Treinos"

    def save(self, *args, **kwargs):
        if self.ficha and not self.nome_ficha_backup:
            self.nome_ficha_backup = self.ficha.nome
        super().save(*args, **kwargs)

    def __str__(self):
        nome = self.nome_ficha_backup or "Treino Desconhecido"
        return f"{nome} concluído em {self.realizado_em.strftime('%d/%m/%Y')}"