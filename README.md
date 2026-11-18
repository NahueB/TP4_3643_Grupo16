# TP4 Integrador – Redes de Computadoras 3643 (UNLaM) – Grupo 16

Scripts de Python que consumen la **Northbound REST API del Network Controller de Cisco Packet Tracer**
(Actividad 4 del TP N°4 Integrador, 2° cuatrimestre 2026, Comisión 02).

**Integrantes (Grupo 16):** BATTISTELLI, Nahuel · CARTASEGNA, Nahuel Nicolás · SÁNCHEZ, Nahuel Alejandro

## Qué hay en el repositorio

| Archivo | Descripción |
|---|---|
| `src/01_get-ticket.py` | `POST /ticket`: obtiene el *service ticket* y lo guarda en `.ticket` (ignorado por git). |
| `src/02_get-network-device.py` | `GET /network-device`: lista hostname, plataforma e IP de gestión de cada equipo. |
| `src/03_get-host.py` | `GET /host`: lista hostname, IP, MAC y puerto de conexión de cada host. |
| `src/04_tabulate.py` | Script de la cátedra (con `tabulate`): tablas de dispositivos y hosts. |
| `src/05_inventario_csv.py` | **Script propio**: consulta `/network-device`, `/host` y `/discovery` y genera tres CSV de inventario (`inventario_dispositivos.csv`, `inventario_hosts.csv`, `inventario_discovery.csv`) más un resumen con la cantidad de equipos *Managed*. |
| `requirements.txt` | Dependencias (`requests`, `tabulate`). |

## Requisitos previos

1. Cisco Packet Tracer abierto con el archivo `TP4_3643_Grupo16.pkt`.
2. En Packet Tracer: **Options → Preferences → Miscellaneous → Enable External Access for Network Controller REST API**.
3. En el controlador (`NC-Grupo16`): pestaña **Config → REAL WORLD → Controller → Access Enabled** con *HTTP Port* `58000`
   (el estado debe decir *Listening on port 58000*).
4. Haber hecho el Discovery desde la interfaz web del controlador (`http://10.16.30.5`), para que la API devuelva equipos.
5. Python 3.10 o superior.

## Instalación (entorno virtual)

El entorno virtual **no** se versiona (está en `.gitignore`); cada uno lo crea en su máquina.

```bash
git clone https://github.com/NahueB/TP4_3643_Grupo16.git
cd TP4_3643_Grupo16

python -m venv .venv
# Windows (PowerShell / CMD)
.venv\Scripts\activate
# Linux / macOS
# source .venv/bin/activate

pip install -r requirements.txt
```

## Uso

Los scripts apuntan a `http://localhost:58000/api/v1`. Las credenciales de laboratorio del controlador
(`cisco` / `class`) se pueden cambiar con las variables de entorno `NC_USER` y `NC_PASS`.

```bash
python src/01_get-ticket.py          # genera el ticket y lo guarda en src/.ticket
python src/02_get-network-device.py  # usa el ticket guardado (o la variable NC_TICKET)
python src/03_get-host.py
python src/04_tabulate.py            # pide su propio ticket
python src/05_inventario_csv.py      # pide su propio ticket y genera los CSV en la carpeta src/
```

Salida esperada con la topología del TP4: **11 dispositivos de red** (9 en estado *Managed*, el ISP en
*Wrong credential* y el controlador docente en *Unsupported*) y **9 hosts**.

## Notas

- El ticket dura 3600 s (sesión) y 900 s sin actividad; si la API responde 401/403, volver a ejecutar `01_get-ticket.py`.
- Las credenciales incluidas son las del laboratorio de Packet Tracer (no hay datos reales).
- Los `.csv` generados, `.ticket`, `.venv/` y `__pycache__/` están en `.gitignore`.
