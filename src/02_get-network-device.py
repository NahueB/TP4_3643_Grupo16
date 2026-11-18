# 02 - Lista los dispositivos de red (GET /network-device)
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

api_url = "http://localhost:58000/api/v1/network-device"

headers = {"X-Auth-Token": leer_ticket()}

resp = requests.get(api_url, headers=headers)

print("Request status: ", resp.status_code)

response_json = resp.json()
networkDevices = response_json["response"]
print("Dispositivos devueltos: ", len(networkDevices))
print()

# .get() porque algunos dispositivos (p. ej. el ISP o el controlador docente) pueden no traer todos los campos
for networkDevice in networkDevices:
    print(networkDevice.get("hostname", "-"), "\t", networkDevice.get("platformId", "-"), "\t", networkDevice.get("managementIpAddress", "-"))
