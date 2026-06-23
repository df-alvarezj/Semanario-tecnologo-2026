# FinTech Nova — Motor de Riesgo Crediticio

> API de evaluación de créditos — Roslaysoft Consulting

## Integrantes del Grupo

| Nombre | GitHub User | Rol |
|----------|----------|----------|
| Daniel_Alvarez | @df-alvarezj | Desarrollador |

## Laboratorio 1 — Estado: COMPLETADO

### URL del Codespace

https://curly-capybara-96gxw6rxqjv37j9v-8000.app.github.dev/

### Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|----------|----------|
| /status | GET | Health check |
| /evaluar-riesgo | POST | Motor de riesgo |
| /datos-financieros/{id} | GET | Vulnerable |

### Diagrama Arquitectónico As-Is

![Arquitectura](docs/diagramas/arquitectura_as_is_lab1.png)

## Cómo ejecutar

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload