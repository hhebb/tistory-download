import argparse
import json
import webbrowser
import requests
import sys

    
# 로그인
def login(url='/oauth/authorize'):
    url = 'https://www.tistory.com' + url
    params = {
        'client_id':my_info['client_id'],
        'redirect_uri':my_info['redirect_uri'],
        'response_type':my_info['response_type'],
        'state':''
    }
    res = requests.get(url, params)
    webbrowser.open(res.url)

# 토큰 획득
def get_token(url='/oauth/access_token', code=None):
    url_token = 'https://www.tistory.com' + url
    params_token = {
        'client_id':my_info['client_id'],
        'client_secret':my_info['client_secret'],
        'redirect_uri':my_info['redirect_uri'],
        'code':code,
        'grant_type':'authorization_code'
    }
    res_token = requests.get(url_token, params_token)
    token = res_token.text.split('=')[1]
    return token

def get_categories(url='/apis/category/list', token=None):
    url = 'https://www.tistory.com' + url
    params = {
        'access_token': token,
        'output':'json',
        'blogName':'weflug'
    }

    res = requests.get(url, params)
    res = res.json()
    category_list = list(map(lambda x:x['name'], res['tistory']['item']['categories']))
    return category_list


def read_post(url='/apis/post/read', token=None):
    url = 'https://www.tistory.com' + url
    params = {
        'access_token': token,
        'output':'json',
        'blogName':'weflug',
        'postId':215
    }

    res = requests.get(url, params)
    res = res.json()
    document = res['tistory']['item']
    document['categoryId'], document['content'], document['title']
    
if __name__ == "__main__":
    # 정보 로드
    with open('info.json', 'r') as f:
        text = f.read()
        my_info = json.loads(text)
    
    
    login()
    code = input()
    token = get_token(code=code)
    
    category_list = get_categories(token=token)
    print(category_list)
    