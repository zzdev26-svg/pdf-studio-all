# PDF Studio

SaaS simple de una sola página: subís un PDF y obtenés el Markdown equivalente, listo para que lo consuma un agente de IA.

## Stack

- Backend: FastAPI + [pymupdf4llm](https://pypi.org/project/pymupdf4llm/) (extracción de PDF a Markdown preservando tablas/headers).
- Frontend: una única página HTML/CSS/JS vanilla en `static/index.html`.

## Desarrollo local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Abrir http://localhost:8000

## Próximos pasos (no implementados aún)

- Integración con agentes de IA (enviar el markdown generado directamente a un agente).
- Persistencia / historial de conversiones.
- Auth y límites por usuario si se expone públicamente.
