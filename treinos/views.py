from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm # <- ESTA LINHA ESTÁ FALTANDO!
from .models import Mensagem, Exercicio
from .forms import ExercicioForm, LoginForm

def index(request):
    mensagens = Mensagem.objects.all()
    
    # SE ESTIVER LOGADO, FILTRA APENAS OS EXERCÍCIOS DELE. SE NÃO, RETORNA VAZIO.
    if request.user.is_authenticated:
        exercicios = Exercicio.objects.filter(usuario=request.user)
    else:
        exercicios = []
        
    return render(request, "home/index.html", {
        "mensagens": mensagens, 
        "exercicios": exercicios
    })


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

def logout_usuario(request):
    auth_logout(request)
    return redirect('index')