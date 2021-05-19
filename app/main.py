import os
import json
from typing import Optional
from requests import post,get
from fastapi import FastAPI

app = FastAPI()

ha_ip = os.environ['HA_IP'] 
ha_port = os.environ['HA_PORT'] 
ha_entity = os.environ['HA_ENTITY'] #must be a sensor
ha_token = os.environ['HA_TOKEN']
ha_friendly_name = os.environ['HA_FRIENDLY_NAME']
ha_domain = ha_entity.split('.')[0]
if not ha_domain.lower() == "sensor":
    print("Specify a sensor as HA_ENTITY")
    exit()

base_url = str("http://" + ha_ip + ":" + ha_port + "/api/states/" + ha_entity)
headers = {
    "Authorization": str("Bearer " + ha_token),
    "Content-Type": "application/json"
}

def get_current_value():
    cur_val = json.loads(get(base_url, headers=headers).text)
    return cur_val["attributes"]["status"], cur_val["attributes"]["activity"]

@app.post("/status/{status}")
def catch_status(status:str):
    null,activity = get_current_value()
    payload = {"state":status,"attributes":{"activity":activity,"status":status,"friendly_name":ha_friendly_name,"unit_of_measurement":""}}
    print(payload)
    post(base_url,headers=headers,json=payload)

@app.post("/activity/{activity}")
def catch_activity(activity:str):
    status,null = get_current_value()
    payload = {"state":status,"attributes":{"activity":activity,"status":status,"friendly_name":ha_friendly_name,"unit_of_measurement":""}}
    print(payload)
    post(base_url,headers=headers,json=payload)
