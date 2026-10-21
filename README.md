# Academia Corpo em Movimento

Sistema web em Django com painel administrativo (modalidades e turmas) e duas páginas públicas
(`/` e `/turmas/`), lidas direto do banco de dados.

## Equipe
- Arthur Henrique da Silva Vieira
  

## Como rodar
```bash
python -m venv venv
# Windows:  venv\Scripts\activate      |  Linux/Mac:  source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser        # cria o usuário do painel
python manage.py carregar_dados         # (opcional) carrega os dados iniciais do documento
python manage.py runserver
```
- Painel: http://127.0.0.1:8000/admin/
- Página inicial: http://127.0.0.1:8000/
- Grade de turmas: http://127.0.0.1:8000/turmas/

Testes automáticos: `python manage.py test`

## Decisões
- **Endereço e telefone** da academia não constavam no documento: usei valores provisórios, ficam em `ACADEMIA` no `config/settings.py` e é só trocar.
- **Dia da semana** guardado como número (1 a 6) com rótulo (Segunda a Sábado), para ordenar a grade corretamente.
- **/turmas/** mostra todas as turmas, inclusive de modalidade inativa (o documento só esconde modalidade inativa na página inicial).
- **RN03** implementada com `on_delete=PROTECT`: o banco impede excluir modalidade que tenha turmas.
- **Dados iniciais**: comando `carregar_dados` (seção 7 do documento); também podem ser cadastrados manualmente pelo painel.
- **Django 5.2 LTS**, por rodar em versões mais antigas do Python (3.10+).

## Diário de IA
Use da IA: Claude (Anthropic).
- **O que pedi:** gerar o projeto Django a partir do documento de requisitos, com explicação de cada parte.
- **O que a IA fez:** estrutura do projeto, modelos, painel admin, views, templates, comando de carga de dados e testes.
- **O que eu conferi:** rodei os testes, cadastrei/exclui dados pelo painel, testei filtros, busca e a regra RN03, e li o código para entender cada parte.
- E assim finalizei.
  
