import requests
import csv
import pandas as pd

posts=2000 #количество постов сообщества
def take_posts():
    """
    Данная функция собирает все посты в один список json файлов 
    
    """
    api_key='33623ba633623ba633623ba6b7331f1d503336233623ba651d6b46925932c22a130985e'
    domain = 'iamplc'
    count=100#столько постов за раз выдаёт один запрос к vk api
    offset = 0#сдвиг для того, чтобы получить следующие 100 записей сообщества
    posts_list=[]
    
    while offset<posts:#количество постов
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    "access_token": api_key,
                                    "v":5.92,
                                    "domain": domain,
                                    "count":count,
                                    "offset":offset
                                    })
        data = response.json()["response"]["items"]#100 последних постов
        offset+=100
        posts_list.extend(data)
    return posts_list


def file_writer(all_posts):
    """
    Данная функция записывает в csv файл для каждого поста 
    количество лайков и текст поста
    """
  

    dictionaries=[]
    headers = ['likes', 'text']
    for post in all_posts:
        d={}
        d['likes']=post['likes']['count']
        d['text']=post['text']
        dictionaries.append(d)
    with open('all_posts.csv', 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()
        writer.writerows(dictionaries)
               
all_posts = take_posts()
file_writer(all_posts)
with open('all_posts.csv','r', encoding="utf-8") as file:
    data = pd.read_csv(file)
  
    max_likes=data['likes'].max()
    print(f'Самая популярная запись сообщества набрала {max_likes} лайков')
    print('Текст записи:')
    print(data[data['likes']==max_likes]['text'].item())
        