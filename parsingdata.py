import json

async def  config(self):
    with open('config.json', 'r') as f:
        return json.load(f)