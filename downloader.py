import argparse
import json
import webbrowser
import requests
import sys
import time
    
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


def download_post(token, cnt):
    url = 'https://www.tistory.com/apis/post/read'
    params = {
        'access_token': token,
        'output':'json',
        'blogName':'weflug',
        'postId':cnt
    }

    res = requests.get(url, params)
    res = res.json()
    try:
        document = res['tistory']['item']
        document['categoryId'], document['content'], document['title']

        with open(f'post_{cnt}.html', 'w') as f:
            f.write(document['content'])
            pass
        return document['title']
    except:
        return -1
    

def get_total_count(token):
    url = 'https://www.tistory.com/apis/blog/info'
    params = {
        'access_token':token,
        'output':'json'
    }

    res = requests.get(url, params)
    blog_info = res.json()
    total_post = blog_info['tistory']['item']['blogs'][1]['statistics']['post']
    return total_post
    
def download_all_posts(token):
    cnt = 1
    inc = 1
    total_post = get_total_count(token)
    while cnt <= int(total_post):
        post_entry = download_post(token, inc)
        if post_entry != -1:
            #print(post_entry)
            cnt += 1
        inc += 1
    
if __name__ == "__main__":
    # 정보 로드
    with open('info.json', 'r') as f:
        text = f.read()
        my_info = json.loads(text)
    
    
    login()
    code = sys.stdin.readline().strip()
    token = get_token(code=code)
    
    category_list = get_categories(token=token)
    #print(category_list)
    
    print('wanna download?: ', flush=True)
    ans = sys.stdin.readline().strip()
    
    if ans == 'y' or ans == 'yes':
        print('downloading...')
        download_all_posts(token)
    else:
        pass
    
    print(f'completed')