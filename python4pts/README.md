# Painel de Controle de Tarefas

Atividade prática de Flask (CRUD de tarefas com autenticação, integração com API
externa, filtro em tempo real, modo escuro, dashboard de progresso e API REST).

## Estrutura (padrão MVC)

```
app.py                      → cria e configura a aplicação Flask
models/                     → tabelas do banco (SQLAlchemy)
    usuario.py               usuarios (id, nome, email, senha em hash)
    tarefa.py                tarefas (id, titulo, descricao, status, usuario_id)
controllers/                → rotas, organizadas por assunto (Blueprints)
    auth_controller.py       /registro, /login, /logout
    tarefas_controller.py    /dashboard, /nova_tarefa, /editar/<id>, /excluir/<id>
    progresso_controller.py  /progresso (gráficos)
    api/api_v1_controller.py /api/v1/... (JSON: filtro, CRUD REST, progresso)
services/                   → integrações externas
    advice_api.py             busca a frase motivacional do dia
views/
    templates/                HTML (Jinja2 + Bootstrap 5)
    static/                   CSS e JavaScript
```

## Como rodar

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # ajuste SECRET_KEY se quiser
python app.py
```

Acesse http://127.0.0.1:5000 — a rota raiz redireciona para o dashboard (ou
para o login, se você ainda não tiver entrado).

## O que foi implementado, item a item

1. **Estrutura inicial** — app modular (`app.py`, `models/`, `controllers/`,
   `services/`, `views/templates`, `views/static`), com `layout.html` como
   template base.
2. **Banco de dados** — SQLite via SQLAlchemy, tabelas `usuarios` e `tarefas`
   com relacionamento 1‑N (`Usuario.tarefas`).
3. **Autenticação** — `/registro`, `/login`, `/logout`; senha guardada como
   hash (`werkzeug.security`); rotas internas protegidas com um decorator
   `login_required` que usa `session`.
4. **Integração com API externa** — o dashboard mostra uma frase motivacional
   vinda de `https://api.adviceslip.com/advice` (com frase de reserva caso a
   API externa esteja fora do ar).
5. **CRUD de tarefas** — `/dashboard` (listar), `/nova_tarefa` (criar),
   `/editar/<id>`, `/excluir/<id>`.
6. **Interface e estilo** — Bootstrap 5 + Bootstrap Icons, cards responsivos.
7. **Segurança** — `SECRET_KEY` via variável de ambiente, `FLASK_DEBUG`
   controlando o modo debug, senhas em hash, validação dos formulários.
8. **Filtro por status** — dropdown na tela de tarefas que consulta
   `GET /api/v1/tarefas?status=...` via `fetch()` e redesenha a lista sem
   recarregar a página. As cores seguem o desafio proposto: pendente =
   amarelo, em andamento = azul, concluída = verde.
9. **Modo escuro** — botão que alterna `data-bs-theme` do Bootstrap e salva a
   preferência em `localStorage`, aplicada automaticamente ao recarregar.
10. **Dashboard de progresso** — página `/progresso` com dois gráficos
    Chart.js (barras e pizza) alimentados por `GET /api/v1/progresso`.

    > Obs.: o enunciado pede uma página adicional em `/dashboard`, mas essa
    > rota já é usada pelo painel principal de tarefas (item 5). Para não
    > colidir, o dashboard de progresso ficou em `/progresso` — está
    > comentado no `progresso_controller.py`.

**Desafio Avançado** — API REST completa em `/api/v1/tarefas`
(`GET`/`POST`/`PUT`/`DELETE`). O front-end consome essas rotas com
`fetch()` para excluir e marcar tarefas como concluídas sem recarregar a
página (veja `views/static/js/main.js`).
