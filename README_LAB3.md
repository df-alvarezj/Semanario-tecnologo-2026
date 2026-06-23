# Lab 3 — Automatización, Observabilidad y Contenedores
**Proyecto:** FinTech Nova — API de Evaluación Crediticia  
**Sesión:** 13 | Integración: Scripting → Health Checks → Docker

---

## Prerequisitos
- Git instalado
- Docker instalado (`docker --version` para verificar)
- Python 3.11+
- GitHub Codespaces (o cualquier servidor Linux)

---

## Configuración Inicial

```bash
# 1. Clonar el repositorio
git clone https://github.com/df-alvarezj/Semanario-tecnologo-2026.git
cd Semanario-tecnologo-2026

# 2. Cambiar a la rama del lab
git checkout lab3-automatizacion-docker

# 3. Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Bloque 1 — Scripts de Automatización

### backup_db.sh — Backup automático de la base de datos
```bash
# Dar permisos y ejecutar
chmod +x backup_db.sh
./backup_db.sh

# Verificar que el backup se creó
ls -lh backups/
```

### Automatizar con Cron (cada día a las 2AM)
```bash
crontab -e
# Agregar esta línea:
0 2 * * * /workspaces/Semanario-tecnologo-2026/backup_db.sh >> /tmp/backup.log 2>&1

# Verificar que quedó guardado
crontab -l
```

### log_analyzer.py — Detector de SQL Injection
```bash
python3 log_analyzer.py server.log
```

### resource_monitor.sh — Monitor de recursos del sistema
```bash
chmod +x resource_monitor.sh
./resource_monitor.sh
```

---

## Bloque 2 — Observabilidad

### Iniciar la API localmente
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Consultar el Health Check
```bash
curl -s http://localhost:8000/health | python3 -m json.tool
```

### Respuesta esperada
```json
{
  "status": "healthy",
  "checks": {
    "database": {"status": "ok"},
    "disk":     {"status": "ok"},
    "backup":   {"status": "ok"},
    "memory":   {"status": "ok"}
  }
}
```

---

## Bloque 3 — Contenedor Docker

### Construir la imagen
```bash
docker build -t fintech-nova:1.0 .
```

### Ejecutar el contenedor
```bash
docker run -d -p 8000:8000 --name fintech-api fintech-nova:1.0
```

### Verificar que está corriendo
```bash
docker ps
curl -s http://localhost:8000/health | python3 -m json.tool
```

### Ver logs del contenedor
```bash
docker logs -f fintech-api
```

### Detener y eliminar el contenedor
```bash
docker stop fintech-api
docker rm fintech-api
```

---

## Solución de Problemas

**ERROR: `port is already allocated`**  
El puerto 8000 ya está en uso por uvicorn local.  
Solución: `pkill -f uvicorn` antes de ejecutar el contenedor.

**ERROR: `ModuleNotFoundError` al iniciar el contenedor**  
Falta una librería en requirements.txt.  
Solución: `pip freeze > requirements.txt` y reconstruir con `docker build`.

**ERROR: Health check siempre en `starting` o `unhealthy`**  
El endpoint /health no responde dentro del contenedor.  
Diagnóstico: `docker exec -it fintech-api curl -v http://localhost:8000/health`

---

## Archivos del Laboratorio

| Archivo | Descripción |
|---------|-------------|
| `backup_db.sh` | Backup automático de database.db con retención 7 días |
| `log_analyzer.py` | Detecta intentos de SQL Injection en server.log |
| `health_check.py` | Verifica BD, disco, backup y memoria RAM |
| `resource_monitor.sh` | Monitor de uso de CPU, RAM y disco |
| `Dockerfile` | Empaqueta la API en contenedor seguro con usuario no-root |
| `.dockerignore` | Excluye archivos innecesarios de la imagen Docker |