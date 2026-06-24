# Lab 4 — CI/CD Pipeline con GitHub Actions y DevSecOps

> **Sesión 14 · FinTech Nova · Automatización del flujo de entrega con controles de seguridad Shift-Left**

---

## Información del Lab

| Campo | Detalle |
|-------|---------|
| **Rama** | `lab4-cicd-devops` |
| **Sesión** | 14 — CI/CD y Despliegue Continuo |
| **Prerequisitos** | Lab 2 (hardening-api) · Lab 3 (docker) |
| **Herramientas** | GitHub Actions · pip-audit · Docker |
| **Tiempo estimado** | 45–60 minutos |

---

## Objetivo

Implementar un pipeline CI/CD automatizado que integra controles de seguridad **Shift-Left**, de modo que ningún código con vulnerabilidades conocidas pueda llegar a producción.

---

## Estructura de Archivos Creados

```
fintech-nova/
│
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yml   ← ⭐ El pipeline que creamos
│
├── app/                         ← Código de la API (labs anteriores)
├── Dockerfile                   ← Del Lab 3
└── requirements.txt             ← Dependencias de Python
```

---

## Pasos del Pipeline

El pipeline se activa automáticamente con cada `git push` a la rama `main` y ejecuta 5 pasos en secuencia:

```
PUSH → [A] Checkout → [B] Python 3.11 → [C] Dependencias → [D] pip-audit 🔒 → [E] Docker Build 🐳
                                                                     ↓
                                                            Si falla → ❌ STOP
                                                            (código no avanza)
```

| Paso | Nombre | Propósito |
|------|--------|-----------|
| **A** | Checkout | Descarga el código a la VM de GitHub |
| **B** | Configurar Python 3.11 | Garantiza la versión exacta del entorno |
| **C** | Instalar dependencias | `pip install -r requirements.txt` |
| **D** | **pip-audit** 🔒 | Auditoría de seguridad — **Shift-Left** |
| **E** | Docker build | Construye la imagen etiquetada con el SHA del commit |

---

## Comandos para Ejecutar el Lab

### 1. Crear y cambiar a la rama del lab
```bash
git checkout -b lab4-cicd-devops
```

### 2. Crear la estructura de carpetas
```bash
mkdir -p .github/workflows
```

### 3. Crear el archivo del pipeline
Copia el contenido de `.github/workflows/ci-cd-pipeline.yml` a esa ruta.

### 4. Subir los cambios y activar el pipeline
```bash
git status
git add .github/workflows/ci-cd-pipeline.yml
git commit -m "feat: agregar pipeline CI/CD con auditoría de seguridad pip-audit"
git push origin lab4-cicd-devops
```

> ⚠️ **Nota:** Si el pipeline está configurado para activarse en `main`, deberás hacer un Pull Request desde `lab4-cicd-devops` → `main`, o ajustar el disparador para incluir tu rama durante el desarrollo.

---

## Monitorear el Pipeline en GitHub

1. Abre tu repositorio en **github.com**
2. Haz clic en la pestaña **Actions**
3. Selecciona la ejecución más reciente

### Estados posibles

| Icono | Estado | Significado |
|-------|--------|-------------|
| 🟡 | En progreso | El pipeline está corriendo — puedes ver logs en tiempo real |
| ✅ | Exitoso | Todo pasó. Imagen Docker construida y verificada. |
| ❌ | Fallido | Algún paso falló. El código **no** avanzó. Lee los logs. |

---

## DevSecOps en Acción: pip-audit

`pip-audit` compara las dependencias de `requirements.txt` contra las bases de datos de vulnerabilidades **OSV** (Google) y **NVD** (gobierno de EE.UU.).

### Ejemplo de vulnerabilidad detectada
```
requests 2.25.0 affected by GHSA-j8r2-6x86-q33q
Fixed in: requests 2.31.0
Error: pip-audit exited with code 1
```

**Cómo corregirlo:** En `requirements.txt`, cambia:
```
requests==2.25.0   # ❌ vulnerable
```
por:
```
requests==2.31.0   # ✅ seguro
```
Luego: `git add requirements.txt && git commit -m "fix: actualizar requests a versión segura" && git push`

---

## Conceptos Clave Aplicados

| Concepto | Implementación en este lab |
|----------|--------------------------|
| **CI (Integración Continua)** | Pipeline se ejecuta en cada push automáticamente |
| **DevSecOps** | pip-audit integrado como guardián de seguridad |
| **Shift-Left** | Seguridad verificada *antes* de construir la imagen |
| **Romper el Build** | Pipeline se detiene si pip-audit detecta vulnerabilidades |
| **Trazabilidad** | Imagen etiquetada con `${{ github.sha }}` |

---

## Conexión con Labs Anteriores

| Lab | Lo que aportó | Cómo se usa aquí |
|-----|--------------|------------------|
| **Lab 2** — Hardening API | API Flask con controles de seguridad | El código que el pipeline protege y verifica |
| **Lab 3** — Docker | `Dockerfile` funcional | El pipeline usa este Dockerfile en el Paso E |
| **Lab 4** — CI/CD *(este)* | Pipeline GitHub Actions + pip-audit | Orquesta y automatiza todo el proceso |

---

## Criterios de Éxito

- [ ] Archivo `.github/workflows/ci-cd-pipeline.yml` creado con indentación correcta
- [ ] Pipeline visible en la pestaña **Actions** del repositorio
- [ ] Al menos una ejecución con estado ✅ **Exitoso**
- [ ] pip-audit corrió sin encontrar vulnerabilidades (o las corregiste)
- [ ] Imagen Docker construida con tag `fintech-nova:<SHA>`

---

## Ejercicio Extra (Opcional)

Agrega un paso de análisis estático con **Bandit** (herramienta de seguridad para Python):

```yaml
- name: "🛡️ Análisis Estático de Seguridad (Bandit)"
  run: |
    pip install bandit
    bandit -r app/ -ll
```

Inserta este paso **antes** del paso de Docker build. El flag `-ll` hace que Bandit solo rompa el build en vulnerabilidades de **severidad media o alta**.

---

*Lab 4 — Sesión 14 · FinTech Nova · CI/CD y DevSecOps*