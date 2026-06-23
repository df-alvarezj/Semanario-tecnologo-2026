#!/usr/bin/env python3
"""
health_check.py — Verificación de salud para FinTech Nova
Lab 3 - Sesión 13
"""
import sqlite3
import shutil
import os
import time
from datetime import datetime
from typing import Tuple
import psutil

def check_memory() -> Tuple[str, str]:
    try:
        memory = psutil.virtual_memory()
        used_pct = memory.percent
        available_gb = memory.available / (1024**3)
        if used_pct >= 90:
            return 'error',   f'RAM crítica: {used_pct:.1f}% usada ({available_gb:.1f}GB disponible)'
        if used_pct >= 75:
            return 'warning', f'RAM alta: {used_pct:.1f}% usada ({available_gb:.1f}GB disponible)'
        return 'ok', f'RAM saludable: {used_pct:.1f}% usada ({available_gb:.1f}GB disponible)'
    except Exception as e:
        return 'error', f'No se pudo verificar memoria: {e}'

def check_database(db_path: str = 'database.db') -> Tuple[str, str]:
    if not os.path.exists(db_path):
        return 'error', f'Archivo de BD no encontrado: {db_path}'
    try:
        start = time.time()
        conn = sqlite3.connect(db_path, timeout=5)
        conn.execute('SELECT 1')
        conn.close()
        elapsed_ms = (time.time() - start) * 1000
        if elapsed_ms > 500:
            return 'warning', f'BD lenta: {elapsed_ms:.1f}ms (límite: 500ms)'
        return 'ok', f'BD accesible y respondiendo en {elapsed_ms:.1f}ms'
    except sqlite3.OperationalError as e:
        return 'error', f'Error al conectar con BD: {e}'

def check_disk(path: str = '/', warn_pct: int = 80, crit_pct: int = 95):
    try:
        usage = shutil.disk_usage(path)
        used_pct = (usage.used / usage.total) * 100
        free_gb  = usage.free / (1024**3)
        if used_pct >= crit_pct:
            return 'error',   f'Disco crítico: {used_pct:.1f}% usado ({free_gb:.1f}GB libre)'
        if used_pct >= warn_pct:
            return 'warning', f'Disco alto: {used_pct:.1f}% usado ({free_gb:.1f}GB libre)'
        return 'ok', f'Disco saludable: {used_pct:.1f}% usado ({free_gb:.1f}GB libre)'
    except Exception as e:
        return 'error', f'No se pudo verificar disco: {e}'

def check_backup(backup_dir: str = 'backups', max_age_hours: int = 25):
    if not os.path.isdir(backup_dir):
        return 'warning', f'Directorio de backups no existe: {backup_dir}'
    backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.tar.gz')])
    if not backups:
        return 'error', 'No se encontraron backups en el directorio'
    latest      = backups[-1]
    latest_path = os.path.join(backup_dir, latest)
    age_hours   = (time.time() - os.path.getmtime(latest_path)) / 3600
    if age_hours > max_age_hours:
        return 'warning', f'Backup más reciente tiene {age_hours:.1f}h (máx: {max_age_hours}h)'
    return 'ok', f'Backup reciente: {latest} ({age_hours:.1f}h de antigüedad)'

def run_all_checks() -> dict:
    checks = {}

    db_status,  db_msg  = check_database()
    disk_status, disk_msg = check_disk()
    bkp_status, bkp_msg = check_backup()
    mem_status, mem_msg   = check_memory()

    checks['database'] = {'status': db_status,   'message': db_msg}
    checks['disk']     = {'status': disk_status,  'message': disk_msg}
    checks['backup']   = {'status': bkp_status,   'message': bkp_msg}
    checks['memory']   = {'status': mem_status,  'message': mem_msg}

    all_statuses = [checks[k]['status'] for k in checks]
    if 'error'   in all_statuses: overall = 'unhealthy'
    elif 'warning' in all_statuses: overall = 'degraded'
    else:                           overall = 'healthy'

    return {
        'status'   : overall,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version'  : '1.0.0',
        'checks'   : checks,
    }

if __name__ == '__main__':
    import json
    result = run_all_checks()
    print(json.dumps(result, indent=2, ensure_ascii=False))