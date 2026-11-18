# 05 - Script propio (TP4): inventario de la red en archivos CSV.
#
# Pide un ticket al Network Controller, consulta tres endpoints (GET /network-device,
# GET /host y GET /discovery) y genera:
#   - inventario_dispositivos.csv : hostname, tipo, IP de gestion, plataforma, serie, version, estado
#   - inventario_hosts.csv        : hostname, tipo, IP, MAC, equipo y puerto al que se conecta
#   - inventario_discovery.csv    : id, nombre, tipo, IPs, estado
# Ademas imprime un resumen con la cantidad de equipos Managed y los que no lo estan.
import csv
import json
import os
from datetime import datetime

import requests
from tabulate import tabulate

BASE = "http://localhost:58000/api/v1"
CARPETA = os.path.dirname(os.path.abspath(__file__))


def obtener_ticket():
    cuerpo = {"username": os.environ.get("NC_USER", "cisco"),
              "password": os.environ.get("NC_PASS", "class")}   # credenciales de laboratorio
    r = requests.post(BASE + "/ticket", data=json.dumps(cuerpo),
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()["response"]["serviceTicket"]


def consultar(ruta, ticket):
    r = requests.get(BASE + ruta, headers={"X-Auth-Token": ticket})
    print("GET", ruta, "->", r.status_code)
    r.raise_for_status()
    return r.json()["response"]


def guardar_csv(nombre, encabezado, filas):
    ruta = os.path.join(CARPETA, nombre)
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(encabezado)
        w.writerows(filas)
    print("Archivo generado:", ruta, "(%d filas)" % len(filas))


def main():
    ticket = obtener_ticket()
    print("Ticket:", ticket)
    print("Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()

    dispositivos = consultar("/network-device", ticket)
    filas_d = []
    for d in dispositivos:
        filas_d.append([
            d.get("hostname", ""), d.get("type", ""), d.get("managementIpAddress", ""),
            d.get("platformId", ""), d.get("serialNumber", ""), d.get("softwareVersion", ""),
            d.get("collectionStatus", ""),
        ])
    guardar_csv("inventario_dispositivos.csv",
                ["hostname", "tipo", "ip_gestion", "plataforma", "serie", "version", "estado"], filas_d)

    hosts = consultar("/host", ticket)
    filas_h = []
    for h in hosts:
        filas_h.append([
            h.get("hostName", ""), h.get("hostType", ""), h.get("hostIp", ""), h.get("hostMac", ""),
            h.get("connectedNetworkDeviceIpAddress", ""), h.get("connectedInterfaceName", ""),
        ])
    guardar_csv("inventario_hosts.csv",
                ["hostname", "tipo", "ip", "mac", "equipo_conectado", "puerto"], filas_h)

    discoveries = consultar("/discovery", ticket)
    filas_x = []
    for x in discoveries:
        filas_x.append([x.get("id", ""), x.get("name", ""), x.get("discoveryType", ""),
                        x.get("ipAddressList", ""), x.get("discoveryCondition", "")])
    guardar_csv("inventario_discovery.csv", ["id", "nombre", "tipo", "ips", "estado"], filas_x)

    print()
    print(tabulate([f[:3] + [f[6]] for f in filas_d],
                   headers=["Hostname", "Tipo", "IP gestion", "Estado"], tablefmt="rst"))
    managed = sum(1 for f in filas_d if f[6] == "Managed")
    print("\nDispositivos: %d | Managed: %d | Otros estados: %d" %
          (len(filas_d), managed, len(filas_d) - managed))
    print("Hosts: %d | Discoveries: %d" % (len(filas_h), len(filas_x)))


if __name__ == "__main__":
    main()
