# FitTrack 🏋️‍♂️

- **Nome do Projeto:** FitTrack
- **Integrante:** Jhonata Evangelista da Conceição
- **Repositório:** [https://github.com/jhonatae/fittrack](https://github.com/jhonatae/fittrack)
- **Quadro Kanban:** [https://github.com/users/jhonatae/projects/3](https://github.com/users/jhonatae/projects/3)

## 📝 Descrição do Sistema
O FitTrack é um sistema web voltado para o gerenciamento, estruturação e acompanhamento de rotinas de treinos físicos. A aplicação foi concebida para permitir que os usuários organizem seus exercícios, estruturem fichas de treinamento personalizadas e registrem métricas de evolução corporal e histórico de execução de forma isolada, persistente e segura.

## 🚀 Principais Funcionalidades Implementadas
O sistema expande o modelo tradicional CRUD unindo gerenciamento de dados à regras de domínio específicas para musculação e condicionamento:

1. **Autenticação e Escopo de Usuário:** Sistema completo de cadastro, login e logout. Cada usuário visualiza e gerencia estritamente os seus próprios dados (exercícios e fichas), garantindo privacidade e isolamento na camada do banco de dados.
2. **Catálogo de Exercícios Personalizado:** Permite o cadastro de exercícios associados a grupos musculares específicos (Peitoral, Costas, Membros Inferiores, Braços/Ombros, Abdominais/Core). 
3. **Montagem Dinâmica de Fichas de Treino:** Funcionalidade que permite ao usuário agrupar seus exercícios cadastrados em uma ficha de rotina (ex: *Treino A - Hipertrofia*). Caso o utilizador tente montar uma ficha sem possuir nenhum exercício cadastrado, o sistema valida a regra de negócio e exibe um alerta impeditivo orientando o registro inicial.
4. **Relacionamento Muitos-para-Muitos Customizado:** A associação entre Exercícios e Fichas é feita através de uma tabela intermediária explícita. Isso possibilita que cada exercício adicionado a uma ficha possua metadados exclusivos e customizáveis pelo formulário, como quantidade de **séries**, **repetições** e **carga (kg)**.
5. **Perfil de Utilizador com Cálculo de IMC:** Painel de monitoramento corporal que armazena peso e altura do usuário, executando o cálculo dinâmico do Índice de Massa Corporal (IMC) diretamente na camada de domínio.
6. **Histórico de Treinos Concluídos:** Registro cronológico dos treinos executados com controle de duração em minutos e notas de execução. Possui mecanismo de backup do nome da ficha para manter o histórico íntegro mesmo se a ficha principal for excluída.
7. **Feed do Sistema (Mural de Notificações):** Sistema de mensagens globais lidas do banco de dados, integrado com o painel administrativo e exibido de forma fluida no dashboard.

## 🏗️ Arquitetura do Sistema
O projeto foi estruturado seguindo o padrão **MVT (Model-View-Template)** do Django, rodando em um ambiente totalmente isolado e conteinerizado:
- **Backend / Servidor WEB:** Django 5.1 (Python 3.12)
- **Frontend / Interface:** HTML5 e Tailwind CSS (via CDN) integrado nativamente aos formulários dinâmicos e tags de contexto do Django.
- **Banco de Dados:** SQLite (com persistência local mapeada de forma íntegra via volumes do Docker).
- **Infraestrutura:** Docker e Docker Compose para portabilidade imediata do ambiente.

---

### 🐳 Como Rodar o Projeto com o Docker

Siga as instruções abaixo para clonar, configurar e executar o ambiente de desenvolvimento na sua máquina local.

### Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:
- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (com o Docker Compose ativo)

### 1. Clonar o Repositório

Abra o seu terminal e execute os comandos para clonar o projeto e acessar o diretório correto:


git clone [https://github.com/jhonatae/fittrack.git](https://github.com/jhonatae/fittrack.git)
cd fittrack/demo-django

### 2. Build e Inicialização do Ambiente

docker compose up --build -d

### 3. Clonar o Repositório

# Gerar arquivos de migração para a aplicação (detectar novas tabelas e relacionamentos)
docker compose exec web python manage.py makemigrations

# Aplicar e criar as tabelas de fato no banco de dados
docker compose exec web python manage.py migrate

### 4. Acessar a Aplicação

Dashboard Geral / Home: http://localhost:8000/

Painel Administrativo do Django: http://localhost:8000/admin/

### 5. Criar uma Conta (Cadastro de Usuário)
* Na tela inicial do sistema, clique no botão **"Acessar Painel"**.
* Caso ainda não possua uma conta, clique no link de cadastro na tela de login.
* Preencha o formulário informando seu *Username* e *Senha*.
* Ao salvar, sua conta será criada de forma isolada no banco de dados e você será autenticado automaticamente.

### 6. Adicionar Exercícios ao Catálogo
* Com o seu usuário logado, clique na opção **"Novo Exercício"** localizada no menu superior (Header) da aplicação.
* Preencha o nome do exercício, selecione o Grupo Muscular correspondente (Ex: *Peitoral*) e insira uma descrição curta sobre a forma correta de execução.
* Clique em salvar. O exercício aparecerá imediatamente no seu **Catálogo de Exercícios** no Dashboard. 
* *Nota:* Você pode usar os botões **Editar** ou **Remover** em cada card para gerenciar seu catálogo.

### 7. Montar uma Ficha de Treino Personalizada
* No Dashboard Geral, logo abaixo da sua mensagem de boas-vindas, clique no botão azul **"📋 Montar Ficha de Treino"**.
* *Validação de Segurança:* Se você não tiver cadastrado nenhum exercício no passo anterior, o sistema bloqueará a tela exibindo a mensagem *"Registre algum exercício primeiro!"*.
* Caso possua exercícios no seu catálogo, dê um nome à sua ficha (Ex: *Treino A - Segunda-feira*) e adicione uma descrição/observação geral.
* Abaixo, marque os **Checkboxes** apenas dos exercícios que deseja incluir nesta ficha específica.
* Para cada exercício marcado, configure individualmente o número de **Séries**, **Repetições** e a **Carga (kg)** que pretende levantar.
* Clique em **"Salvar Ficha"**. O sistema irá redirecioná-lo para a tela principal, onde a sua ficha estruturada e detalhada será exibida no painel **"Minhas Fichas de Treino"**.

