import glob
import json
import os

import requests

from sharesio.config import config

properties = []
for file in glob.glob('resources/page_properties/*.json'):
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    with open(file, 'r') as f:
        properties += [f"\"{filename}\": {f.read()}"]

url = f"https://graph.facebook.com/v5.0/me/messenger_profile?access_token={config['page_access_token']}"
body = f"{{{','.join(properties)}}}"
a = requests.post(url, json=json.loads(body))
