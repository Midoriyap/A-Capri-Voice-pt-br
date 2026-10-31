# Capri Voice AI 2.0

Aplicação web mobile + API FastAPI para síntese de voz original em português brasileiro. Dois modos: Natural (voz neural) e Cibernética (mesma voz com filtro e eco). Não clona nem reproduz a voz da personagem/dubladora.

## Publicar usando apenas Android

1. No Chrome, entre em https://github.com e crie um repositório.
2. Envie os arquivos `main.py`, `requirements.txt`, `Dockerfile`, `render.yaml` e a pasta `static` (com `index.html`) para a raiz do repositório. É possível fazer isso pelo site do GitHub no modo desktop.
3. Entre em https://dashboard.render.com, escolha **New > Web Service**, conecte o repositório e selecione **Docker**. O `render.yaml` também permite usar Blueprint, conforme as opções disponíveis no Render.
4. Aguarde a construção e abra a URL HTTPS fornecida pelo Render no Chrome. O primeiro acesso pode demorar se a instância estiver inativa.
5. Digite um texto, escolha Natural ou Cibernética, clique em **Gerar voz** e reproduza/baixe o MP3.

A API precisa de conexão à internet para acessar o serviço de síntese do edge-tts; disponibilidade e condições do serviço podem mudar. O Render pode alterar planos, cotas e preços.

## API

`POST /api/speak` com JSON:

```json
{"text":"Ei, você chegou. Bem-vindo à cidade do futuro.","style":"cibernetica","speed":0}
```

`style` aceita `natural` ou `cibernetica`; `speed` vai de -30 a +30. A resposta é `audio/mpeg`. Documentação interativa em `/docs`.

## Execução local em computador (opcional)

Requer Python 3.11+ e FFmpeg instalado.

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Abra http://127.0.0.1:8000.
