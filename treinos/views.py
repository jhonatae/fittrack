from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm # <- ESTA LINHA ESTÁ FALTANDO!
from .models import Mensagem, Exercicio
from .forms import ExercicioForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Exercicio, FichaTreino, ItemFichaTreino



@login_required
def montar_ficha(request):
    exercicios_usuario = Exercicio.objects.filter(usuario=request.user)
    
    if not exercicios_usuario.exists():
        return render(request, 'home/montar_ficha.html', {'sem_exercicios': True})
        
    if request.method == 'POST':
        nome_ficha = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        
        # 1. Cria a Ficha
        ficha = FichaTreino.objects.create(
            utilizador=request.user,
            nome=nome_ficha,
            descricao=descricao
        )
        
        # 2. Captura a lista de IDs do formulário
        exercicios_ids = request.POST.getlist('exercicios_selecionados')
        
        # 3. Percorre criando os vínculos explicitamente por ID numérico
        for ex_id in exercicios_ids:
            # Buscamos direto pelo ID numérico enviado convertendo para int
            try:
                exercicio_obj = Exercicio.objects.get(id=int(ex_id))
                
                v_series = request.POST.get(f'series_{ex_id}') or "3"
                v_repeticoes = request.POST.get(f'repeticoes_{ex_id}') or "10"
                v_carga = request.POST.get(f'carga_{ex_id}') or "0"
                
                ItemFichaTreino.objects.create(
                    ficha=ficha,
                    exercicio=exercicio_obj,
                    series=int(v_series),
                    repeticoes=str(v_repeticoes),
                    carga=int(v_carga)
                )
            except (Exercicio.DoesNotExist, ValueError):
                continue
                
        return redirect('index')

    return render(request, 'home/montar_ficha.html', {
        'exercicios': exercicios_usuario,
        'sem_exercicios': False
    })

@login_required
def index(request):
    exercicios = Exercicio.objects.filter(usuario=request.user)
    mensagens = Mensagem.objects.all()
    
    # Mudamos o prefetch para carregar usando o relacionamento reverso correto do model ItemFichaTreino
    fichas = FichaTreino.objects.filter(utilizador=request.user).prefetch_related('itens__exercicio')

    return render(request, 'home/index.html', {
        'exercicios': exercicios,
        'mensagens': mensagens,
        'fichas': fichas,
    })


@login_required
def deletar_ficha(request, pk):
    # Garante que o usuário só consiga deletar as próprias fichas
    ficha = get_object_or_404(FichaTreino, pk=pk, utilizador=request.user)
    
    if request.method == 'POST':
        ficha.delete()
        return redirect('index')
        
    # Se o usuário tentar acessar via GET (pela barra de endereço), 
    # podemos renderizar uma página simples de confirmação ou apenas mandar direto para o index
    return render(request, 'home/deletar_confirmacao.html', {'objeto': ficha, 'tipo': 'ficha'})

def sobre(request):                                   
    return render(request, "home/sobre.html")

    
def cadastrar_exercicio(request):
    # Se um usuário deslogado tentar acessar, joga ele para o login
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ExercicioForm(request.POST)
        if form.is_valid():
            # commit=False impede o Django de salvar no banco imediatamente
            exercicio = form.save(commit=False)
            # Injeta o usuário da sessão atual no exercício
            exercicio.usuario = request.user
            # Agora sim, salva de verdade com o usuário preenchido!
            exercicio.save()
            return redirect('index')
    else:
        form = ExercicioForm()
    
    return render(request, 'home/cadastrar_exercicio.html', {'form': form})
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Cria o usuário criptografado no banco automaticamente!
            return redirect('login') # Redireciona para a tela de login após criar
    else:
        form = UserCreationForm()
    return render(request, 'home/cadastrar_usuario.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})

def editar_exercicio(request, pk):
    # Garante que só quem está logado pode acessar
    if not request.user.is_authenticated:
        return redirect("login")

    # Busca o exercício pelo ID, garantindo que pertença ao usuário logado
    exercicio = get_object_or_404(Exercicio, pk=pk, usuario=request.user)

    if request.method == "POST":
        # Passamos a instância atual para o form saber que deve ATUALIZAR, e não criar um novo
        form = ExercicioForm(request.POST, instance=exercicio)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        # Preenche o formulário com os dados atuais do exercício
        form = ExercicioForm(instance=exercicio)

    return render(request, "home/cadastrar_exercicio.html", {"form": form})


def deletar_exercicio(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")

    # Busca o exercício garantindo a segurança de que pertence ao dono da sessão
    exercicio = get_object_or_404(Exercicio, pk=pk, usuario=request.user)

    if request.method == "POST":
        exercicio.delete()
        return redirect("index")

    # Reaproveitaremos a lógica de confirmação simples de deleção
    return render(
        request, "home/confirmar_exclusao.html", {"exercicio": exercicio}
    )

def logout_usuario(request):
    auth_logout(request)
    return redirect('index')