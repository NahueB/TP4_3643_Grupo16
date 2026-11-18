# 03 - Lista los hosts de la red (GET /host)
# Usa el ticket generado por 01_get-ticket.py (archivo ".ticket") o la variable de entorno NC_TICKET.
import json
import os
import requests

def leer_ticket():
    if os.environ.get("NC_TICKET"):
        return os.environ["NC_TICKET"]
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".ticket")
    with open(ruta) as f:
        return f.read().strip()

api_url = "http://localhost:58000/api/v1/host"

headers = {"X-Auth-Token": leer_ticket()}

resp = requests.get(api_url, headers=headers)

print("Request status: ", resp.status_code)

response_json = resp.json()
hosts = response_json["response"]
print("Hosts devueltos: ", len(hosts))
print()

for host in hosts:
    print(host.get("hostName", "-"), "\t", host.get("hostIp", "-"), "\t", host.get("hostMac", "-"), "\t", host.get("connectedInterfaceName", "-"))
