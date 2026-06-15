# FitTrack

- **Nome do Projeto:** FitTrack
- **Integrante:** Jhonata Evangelista da Conceição
- **Repositório:** [https://github.com/jhonatae/fittrack](https://github.com/jhonatae/fittrack)
- **Quadro Kanban:** [https://github.com/users/jhonatae/projects/3](https://github.com/users/jhonatae/projects/3)

## Descrição
O FitTrack é um sistema WEB voltado para gerenciamento e acompanhamento de treinos físicos. O sistema permite que os usuários organizem seus exercícios, acompanhem sua evolução e registrem informações relacionadas às suas rotinas de atividades físicas de forma isolada e segura.

## Arquitetura do Sistema
O projeto foi estruturado seguindo o padrão MVT (Model-View-Template) do Django, rodando em um ambiente totalmente conteinerizado:
- **Backend / Servidor WEB:** Django 5.1 (Python 3.12)
- **Frontend / Interface:** HTML5 e Tailwind CSS (via CDN) integrado aos formulários dinâmicos do Django
- **Banco de Dados:** SQLite (com persistência local mapeada via volumes do Docker)
- **Infraestrutura:** Docker e Docker Compose

---

### Como Rodar o Projeto com o Docker

Siga as instruções abaixo para clonar, configurar e executar o ambiente de desenvolvimento na sua máquina local.

### Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:
- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (com o Docker Compose ativo)

### 1. Clonar o Repositório

Abra o seu terminal e execute o comando para clonar o projeto na branch principal:

git clone [https://github.com/jhonatae/fittrack.git](https://github.com/jhonatae/fittrack.git)
cd fittrack/demo-django

### 2. Clonar o Repositório

docker compose up -d


### 3. Criar a Estrutura do Banco de Dados (Migrations)

Com os containers rodando, execute os comandos do Django para gerar os arquivos de histórico e aplicar as tabelas estruturais no banco de dados SQLite:


# Gerar arquivos de migração para a app treinos
docker compose exec web python manage.py makemigrations

# Aplicar as tabelas no banco de dados
docker compose exec web python manage.py migrate

### 4. Criar um Usuário Administrador (Superuser)

docker compose exec web python manage.py createsuperuser

### 5. Acessar a Aplicação
Após concluir os passos, abra o seu navegador e acesse:

Dashboard / Home: http://localhost:8000/

Painel Administrativo do Django: http://localhost:8000/admin/
