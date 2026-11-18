# 01 - Obtiene el service ticket del Network Controller (POST /ticket)
# Guarda el ticket en el archivo ".ticket" (ignorado por git) para que lo usen los demas scripts.
import json
import os
import requests

api_url = "http://localhost:58000/api/v1/ticket"

headers = {
    "content-type": "application/json"
}

body_json = {
    "username": os.environ.get("NC_USER", "cisco"),
    "password": os.environ.get("NC_PASS", "class")   # credenciales de laboratorio
}

resp = requests.post(api_url, json.dumps(body_json), headers=headers)

print("Ticket request status: ", resp.status_code)
response_json = resp.json()
print(response_json)
serviceTicket = response_json["response"]["serviceTicket"]

print("The service ticket number is: ", serviceTicket)

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".ticket")
with open(ruta, "w") as f:
    f.write(serviceTicket)
print("Ticket guardado en:", ruta)
