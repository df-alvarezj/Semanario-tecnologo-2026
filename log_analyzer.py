#!/usr/bin/env python3
"""
log_analyzer.py — Detecta intentos de SQL Injection en logs de FinTech Nova
Lab 3 - Sesión 13
"""
import re
import sys
import json
from datetime import datetime
from collections import defaultdict

# ── PATRONES DE DETECCIÓN ───────────────────────────────────
SQL_PATTERNS = [
    (r"'\s*OR\s*'?1'?\s*=\s*'?1", "Bypass de login (OR 1=1)"),
    (r"'\s*--",                    "Comentario SQL para ignorar password"),
    (r"UNION\s+SELECT",            "Exfiltración UNION SELECT"),
    (r"DROP\s+TABLE",              "Destrucción de tabla DROP TABLE"),
    (r"INSERT\s+INTO.*SELECT",     "Inyección de datos"),
    (r"EXEC\s*\(",                 "Ejecución de comandos EXEC"),
]

def analyze_log(log_path: str) -> dict:
    incidents = []
    by_ip   = defaultdict(int)
    by_type = defaultdict(int)
    total_lines = 0

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                total_lines += 1
                line = line.strip()
                if not line:
                    continue

                for pattern, desc in SQL_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        ip_match = re.search(r'IP:(\S+)', line)
                        ip = ip_match.group(1) if ip_match else 'desconocida'
                        incidents.append({
                            'line'   : line_num,
                            'type'   : desc,
                            'ip'     : ip,
                            'content': line[:100],
                        })
                        by_ip[ip]     += 1
                        by_type[desc] += 1
                        break  # una detección por línea es suficiente

    except FileNotFoundError:
        print(f'ERROR: Archivo no encontrado: {log_path}')
        sys.exit(1)
    except PermissionError:
        print(f'ERROR: Sin permisos para leer: {log_path}')
        sys.exit(1)

    return {
        'total_lines': total_lines,
        'clean'      : total_lines - len(incidents),
        'incidents'  : incidents,
        'by_ip'      : dict(by_ip),
        'by_type'    : dict(by_type),
    }

def print_report(results: dict, log_path: str):
    sep = '=' * 60
    print(f'\n{sep}')
    print(f'  REPORTE DE SEGURIDAD — FinTech Nova')
    print(f'  Archivo : {log_path}')
    print(f'  Fecha   : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'{sep}')
    print(f'  Total líneas  : {results["total_lines"]}')
    print(f'  Líneas limpias: {results["clean"]}')
    print(f'  Incidentes    : {len(results["incidents"])}')
    print(f'{sep}\n')

    if results['incidents']:
        print('  INCIDENTES DETECTADOS:')
        for i, inc in enumerate(results['incidents'], 1):
            print(f'  [{i}] Línea {inc["line"]} | {inc["type"]}')
            print(f'       IP: {inc["ip"]}')
            print(f'       {inc["content"][:80]}')
            print()
        print('  IPs más activas:')
        for ip, count in sorted(results['by_ip'].items(), key=lambda x: -x[1]):
            print(f'    {ip}: {count} ataque(s)')
    else:
        print('  Sin incidentes. Logs limpios.')

    print(f'\n{sep}\n')

if __name__ == '__main__':
    log_file = sys.argv[1] if len(sys.argv) > 1 else 'server.log'
    results  = analyze_log(log_file)
    print_report(results, log_file)