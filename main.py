import requests
import json
from datetime import datetime


class VkApi:
    def __init__(self, token):
        self.token = token
        self.photo_count = int(input('Количество фото: '))
        self.id = input('id ')
        self.id_type = None
        try:
            self.id = int(self.id)
            self.id_type = 'int'
        except ValueError:
            self.id_type = 'str'

    def get_photos(self):
        params = {'access_token': self.token,
                  'v': '5.131',
                  'album_id': 'profile',
                  'extended': 1,
                  'photo_sizes': 1,
                  'count': self.photo_count}
        if self.id_type == 'str':
            params['username'] = self.id
        else:
            params['owner_id'] = self.id
        url = 'https://api.vk.com/method/photos.get'
        print('Получение фотогорафий...')
        res = requests.get(url=url, params=params)
        photos_list = list()
        print('Обработка фотографий...')
        for photo in res.json()['response']['items'][0:params['count']]:
            photo_dict = dict()
            photo_dict['date'] = datetime.fromtimestamp(photo['date'])
            photo_dict['likes'] = photo['likes']['count']
            photo_dict['size'] = photo['sizes'][-1]['type']
            photo_dict['url'] = photo['sizes'][-1]['url']
            photos_list.append(photo_dict)
        return photos_list


class YaApi:
    def __init__(self, token, class_name):
        self.token = token
        if isinstance(class_name, VkApi):
            self.class_name = class_name
        else:
            print('Неправильное имя экземпляра класса')

    def upload_photos(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'content type': 'application/json',
                   'authorization': f'OAuth {self.token}'}
        uploaded_photos = list()
        print('Создание папки...')
        folder = requests.put(url=url, headers=headers, params={'path': 'Res_Copy'},)
        print('Загрузка фотографий на диск...')
        for photo in self.class_name.get_photos():
            photo_dict = dict()
            similar = False
            for uploaded_photo in uploaded_photos:
                if uploaded_photo['file_name'] == photo['likes']:
                    similar = True
                    break
            if similar:
                photo_dict['file_name'] = f'{photo["likes"]} {str(photo["date"]).split()[0]}'
            else:
                photo_dict['file_name'] = photo["likes"]
            photo_dict['size'] = [photo['size']]
            params = {'path': f'Res_Copy/{photo_dict["file_name"]}', 'url': photo['url']}
            uploaded_photos.append(photo_dict)
            res = requests.post(url=f'{url}/upload', headers=headers, params=params)
        with open('photos.json', 'w') as file:
            json.dump(uploaded_photos, file)
        print('Фотографии успешно загружены!')

# Использовать upload_photos
