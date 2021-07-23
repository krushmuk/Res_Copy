import requests
import json
from pprint import pprint
from datetime import datetime


class ResCopy:
    def __init__(self, vk_token, vk_id, ya_token):
        self.vk_token = vk_token
        self.vk_id = vk_id
        self.ya_token = ya_token

    def get_photos(self):
        params = {'access_token': self.vk_token,
                  'v': '5.131',
                  'owner_id': self.vk_id,
                  'album_id': 'profile',
                  'extended': 1,
                  'photo_sizes': 1,
                  'count': 2}
        url = 'https://api.vk.com/method/photos.get'
        res = requests.get(url=url, params=params)
        photos_list = list()
        for photo in res.json()['response']['items'][0:params['count']]:
            photo_dict = dict()
            photo_dict['date'] = datetime.fromtimestamp(photo['date'])
            photo_dict['likes'] = photo['likes']['count']
            photo_dict['size'] = photo['sizes'][-1]['type']
            photo_dict['url'] = photo['sizes'][-1]['url']
            photos_list.append(photo_dict)
        return photos_list

    def upload_photos(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'content type': 'application/json',
                   'authorization': f'OAuth {self.ya_token}'}
        uploaded_photos = list()
        folder = requests.put(url=url, headers=headers, params={'path': 'Res_Copy'},)
        print(folder.status_code)
        for photo in self.get_photos():
            photo_dict = dict()
            with open('photos.json') as file:
                photo_json = json.load(file)
                similar = False
                for photo_info in photo_json:
                    if photo_info['file_name'] == photo['likes']:
                        similar = True
                        print(f'{photo_info["file_name"]} is {photo["likes"]}')
                        break
                if similar:
                    photo_dict['file_name'] = f'{photo["likes"]} {str(photo["date"]).split()[0]}'
                else:
                    photo_dict['file_name'] = photo["likes"]
                photo_dict['size'] = [photo['size']]
                params = {'path': f'Res_Copy/{photo_dict["file_name"]}',
                          'url': photo['url']}
                uploaded_photos.append(photo_dict)
                res = requests.post(url=f'{url}/upload', headers=headers, params=params)
                photo_json.append(photo_dict)
                json.dump(photo_json, file)
        print(uploaded_photos)




Copy_my_wall = ResCopy('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
                       1, 'AQAAAAAtiH2ZAADLW6lZpOLkPkX2imAnKXjPmQU')
Copy_my_wall.upload_photos()
