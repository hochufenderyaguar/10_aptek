from params import geocoder_params
from io import BytesIO
import requests
from PIL import Image

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)

if not response:
    pass

json_response = response.json()

org_points = []
for organization in json_response["features"]:
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    point = organization["geometry"]["coordinates"]
    org_point = ','.join(map(str, point))
    if 'круглосуточно' in org_time:
        org_point = f"{org_point},pm2dgl"
    elif org_time:
        org_point = f"{org_point},pm2bll"
    else:
        org_point = f"{org_point},pm2grl"
    org_points.append(org_point)

map_params = {
    "l": "map",
    'pt': ",".join(toponym_coodrinates.split(" ")) + ',round~' + '~'.join(org_points)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"

response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
