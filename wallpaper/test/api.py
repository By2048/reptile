import requests
import json
import pprint

api_code = 'cbf61fb8197d5fdc054041c1bd2945e9'
link = 'https://wall.alphacoders.com/api2.0/get.php?' \
       'auth={0}&method={1}&id={2}&page={3}&info_level={4}' \
    .format(api_code, 'tag', 218, 10, 2)

html_data = requests.get(link).text

json_data = json.loads(html_data)
pprint.pprint(json_data, indent=4)
