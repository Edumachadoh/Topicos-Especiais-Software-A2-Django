#  API RESTful - Jurassic Park (Django)

Uma API RESTful desenvolvida em Python para o gerenciamento de um Parque de Dinossauros. Este projeto implementa relacionamento e fornece operações completas de CRUD (Create, Read, Update, Delete) utilizando os métodos semânticos do protocolo HTTP.

## 🛠️ Tecnologias Utilizadas e Seus Propósitos

* **[Python](https://www.python.org/):** Linguagem base do projeto.
* **[Django](https://www.djangoproject.com/):** Framework web principal. Fornece a base do sistema, o mapeamento objeto-relacional (ORM) para comunicação segura com o banco de dados e o sistema de migrações automáticas.
* **[Django REST Framework (DRF)](https://www.django-rest-framework.org/):** Extensão do Django para APIs. Facilita a criação de rotas, serialização de dados (conversão para JSON) e visualização dos endpoints no navegador.
* **[SQLite](https://www.sqlite.org/):** Banco de dados relacional leve utilizado como padrão para o ambiente de desenvolvimento para o armazenamento de dados.
* **[django-filter](https://django-filter.readthedocs.io/):** Biblioteca integrada ao DRF para permitir a criação de filtros via URL (ex: filtrar especies dinossauros por periculosidade ou parte do nome).
* **[python-dotenv](https://saurabh-kumar.com/python-dotenv/):** Gerenciador de variáveis de ambiente. Garante a segurança do sistema ao ocultar credenciais sensíveis (como a `SECRET_KEY` e senhas de banco) em um arquivo `.env` que não é enviado ao repositório do código.

---

## 🏗️ Arquitetura do Sistema e Camadas

O sistema foi estruturado seguindo boas práticas de isolamento de responsabilidades, dividindo o código em camadas com propósitos únicos e bem definidos:

### 1. Camada de Dados (Models) - `models.py`
Define a estrutura física das tabelas, colunas, tipos de dados e os relacionamentos. 
* **Função:** Usa o ORM do Django para traduzir classes Python em instruções SQL, garantindo a integridade relacional (Chaves Primárias e Estrangeiras) sem a necessidade de escrever SQL manualmente.

### 2. Camada de Tradução (Serializers) - `serializers.py`
É a ponte entre a internet (texto JSON) e o sistema interno (Objetos Python).
* **Função:** Realiza a **desserialização** (valida os dados que entram via POST/PUT antes de chegarem ao banco) e a **serialização** (formata os dados do banco em um JSON limpo para devolver ao usuário), lidando também com o aninhamento de informações de entidades relacionadas.

### 3. Camada de Negócio (Services) - `services.py`
Local que guarda as regras de negócio do sistema. 
* **Função:** Isola as regras de negócio das rotas. Se um dinossauro herbívoro for colocado em uma jaula com um carnívoro a operação não acontece, essa lógica acontece aqui, mantendo a camada de visualização limpa e focada apenas no tráfego HTTP.

### 4. Camada de Visualização (Views/Controllers) - `views.py`
Utiliza os `ModelViewSets` do DRF.
* **Função:** Recebe a requisição HTTP do usuário, identifica qual verbo foi utilizado (GET, POST, etc.) e orquestra a chamada para as outras camadas (chama o Serializer para validar e o Service para salvar). Devolve a resposta com o Status Code adequado (ex: `201 Created`, `404 Not Found`).

### 5. Camada de Filtros (Filters) - `filters.py`
* **Função:** Intercepta as requisições GET para aplicar buscas personalizadas. Permite consultar o banco de dados baseando-se em parâmetros enviados na URL, como limites de valores (`periculosidade_min`, `periculosidade_max`) ou aproximação de texto (`icontains`).

---

## 🚀 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para configurar o ambiente virtual, instalar dependências e rodar o servidor em sua máquina.

### 1. Clonar o Repositório
```bash
git clone https://github.com/SeuUsuario/SeuRepositorio.git
cd SeuRepositorio
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
python -m venv .venv

.venv\Scripts\Activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com sua própria `SECRET_KEY`:
```
SECRET_KEY=sua-chave-secreta-aqui
```

### 5. Aplicar as Migrações e Rodar o Servidor
```bash
python manage.py migrate
python manage.py runserver
```