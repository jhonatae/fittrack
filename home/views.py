from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.contrib import messages
from .forms import MensagemForm
from .models import Mensagem, Tag


def index(request):
    mensagens = Mensagem.objects.all()
    return render(request, "home/index.html", {"mensagens": mensagens})


def sobre(request):
    return render(request, "home/sobre.html")


def nova_mensagem(request):
    if request.method == "POST":
        form = MensagemForm(request.POST)
        if form.is_valid():
            # 1. Salva título, conteúdo, autor e categoria no banco.
            mensagem = form.save()

            # 2. Transforma o texto digitado em objetos Tag e associa à mensagem.
            tags_texto = form.cleaned_data["tags"]
            for pedaco in tags_texto.split(","):
                nome = slugify(pedaco)
                if nome:
                    tag, _ = Tag.objects.get_or_create(nome=nome)
                    mensagem.tags.add(tag)
            if form.is_valid():
                mensagem = form.save()
                # ... laço das tags ...
                messages.success(request, "Mensagem publicada com sucesso!")
                return redirect("index")
            # 3. Redireciona para a página inicial (padrão Post/Redirect/Get).

            return redirect("index")
    else:
        form = MensagemForm()

    return render(request, "home/nova.html", {"form": form})