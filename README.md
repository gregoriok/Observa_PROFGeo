# 🚀 Observa-PROFGeo

Sistema de gestão de dados institucionais focado em Unidades Associadas, Cargos e Turmas.  
Construído inicialmente como um **Monólito (Monolith First)** com Django, mas já preparado para futura migração para um setup **desacoplado API + SPA**.

---

## 🎯 Sobre o Projeto

O **Observa-PROFGeo** é um sistema Web que centraliza e gerencia informações de:

- Coordenação  
- Colaboradores  
- Infraestrutura das Unidades Associadas  

O sistema implementa **controle de acesso**, garantindo que somente *Coordenadores ativos* possam gerenciar cadastros e aprovações de usuários.

---

## 🏗️ Arquitetura Atual — *Monolith First*

- **Frontend:** Templates HTML acoplados ao Django  
- **Backend:** Django Views + ORM

**Vantagem:** Entrega rápida do MVP e deploy simples.  
**Visão Futura:** Migração para:
- Backend Django (API)
- Frontend desacoplado (React/Vue)

---

## 🛠️ Tecnologias Principais

| Categoria            | Tecnologia                    | Uso no Projeto |
|----------------------|-------------------------------|----------------|
| **Backend**          | Python 3.x                    | Linguagem principal |
| **Framework Web**    | Django (Latest LTS)           | Estrutura monolítica, ORM, templates |
| **Autenticação**     | Django Custom User Model      | Login via e-mail e fluxo de aprovação |
| **Banco de Dados**   | PostgreSQL                    | Armazenamento robusto |
| **Estilização**      | Bootstrap 5 + Font Awesome    | Layout via templates |
| **Utils**            | Django Crispy Forms           | Formulários elegantes e responsivos |
| **Deploy (Futuro)**  | Docker + Gunicorn + Nginx     | Ambiente produtivo isolado |

---

## 📦 Estrutura do Módulo de Dados

O sistema é baseado em quatro entidades principais.

### 1. **UnidadeAssociada**
- **Responsabilidade:** dados da unidade (município, estado, status)
- **Funcionalidades:** CRUD completo via interface HTML

### 2. **Usuário (Pessoa)**
- **Responsabilidade:** autenticação e dados pessoais
- **Implementação:** `AbstractBaseUser` customizado  
  - Necessário para o fluxo de aprovação

### 3. **Cargos (Coordenador e Colaborador)**
- Implementação via **One-to-One** com `Usuario`
- **Coordenador:**  
  - Gerencia unidade  
  - Aprova novos cadastros  
- **Colaborador:**  
  - Usuário padrão vinculado a uma UnidadeAssociada

---

## ⚙️ Fluxo e Permissões de Usuário

| Ação                | Permissão Necessária                       | Resultado / Regra |
|--------------------|---------------------------------------------|-------------------|
| **Cadastro**       | Nenhuma                                     | Cria usuário com `ativo=False` e `aprovado_coordenador=False` |
| **Login**          | Usuário ativo **e** aprovado                | Acesso negado se qualquer flag for `False` |
| **Aprovação**      | Coordenador ativo da Unidade ou Superuser   | Define `ativo=True` e `aprovado_coordenador=True` |
| **Gerenciar Unidades** | Coordenador ativo ou Superuser          | Acesso total ao CRUD |
| **Gerenciar Cargos** | Apenas Superuser                          | Vincula coordenadores e colaboradores |

---

## 💻 Configuração do Ambiente de Desenvolvimento

### ✔ Pré-requisitos
- Python **3.11.4+**
- Servidor **PostgreSQL**

---

### 🌀 Passo a Passo

#### 1. **Clonar Repositório**
```bash
git clone https://docs.github.com/pt/repositories/creating-and-managing-repositories/quickstart-for-repositories Observa-PROFGeo
cd Observa-PROFGeo
python -m venv .venv
```
```bash
# Windows
.\.venv\Scripts\activate
```
```bash
# Linux/macOS
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
👉 http://127.0.0.1:8000/
