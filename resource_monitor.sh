#!/bin/bash
# ════════════════════════════════════════════════════════════
# Script: resource_monitor.sh | FinTech Nova | Lab 3 - Ejercicio 1
# Propósito: Verificar uso de CPU, memoria y disco
# ════════════════════════════════════════════════════════════

log() {
  echo "[$(date +"%H:%M:%S")] $1"
}

log "=== Monitor de Recursos FinTech Nova ==="

# ── MEMORIA RAM ──────────────────────────────────────────────
MEMORY_USED=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
log "Memoria RAM usada: ${MEMORY_USED}%"

if [ "$MEMORY_USED" -gt 80 ]; then
  log "WARNING: Memoria alta (${MEMORY_USED}%) — umbral: 80%"
else
  log "OK: Memoria en niveles normales (${MEMORY_USED}%)"
fi

# ── ESPACIO EN DISCO ─────────────────────────────────────────
DISK_USED=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')
log "Disco usado: ${DISK_USED}%"

if [ "$DISK_USED" -gt 85 ]; then
  log "WARNING: Disco alto (${DISK_USED}%) — umbral: 85%"
else
  log "OK: Disco en niveles normales (${DISK_USED}%)"
fi

# ── RESUMEN ──────────────────────────────────────────────────
log "=== Resumen ==="
log "RAM: ${MEMORY_USED}% | Disco: ${DISK_USED}%"
log "Monitor finalizado."