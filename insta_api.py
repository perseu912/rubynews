import requests as rq

def data_ca():
    data_url = 'https://www.instagram.com/casertaoscorpius/?__a=1'
    data_json = rq.get(data_url).json()
    return data_json


# print(data_ca()["seo_category_infos"])