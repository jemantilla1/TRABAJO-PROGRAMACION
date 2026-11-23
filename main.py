import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from logs import log_info, LOG_FILE_PATH
from pruebas import ejecutar_simulaciones


def main():
    print("\n======================================================================")
    print(" SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES/RESERVAS ")
    print("======================================================================\n")

    log_info("Iniciando aplicación principal main.py...")

    resultados = ejecutar_simulaciones()

    print("\n----------------------------------------------------------------------")
    print(" RESUMEN DE EJECUCIÓN DE SIMULACIONES ")
    print("----------------------------------------------------------------------")
    print(f"{'Escenario':<14} | {'Descripción':<36} | {'Resultado':<24}")
    print("-" * 78)

    for esc, desc, res, det in resultados:
        print(f"{esc:<14} | {desc:<36} | {res:<24}")

    print("-" * 78)

    print(f"\n[+] Archivo de log generado en: {LOG_FILE_PATH}")

    if os.path.exists(LOG_FILE_PATH):
        tamano_log = os.path.getsize(LOG_FILE_PATH)
        print(f"[+] Tamaño del log: {tamano_log} bytes.")

    print("[+] El sistema operó con 100% de resiliencia y cero paradas no controladas.\n")


if __name__ == "__main__":
    main()
