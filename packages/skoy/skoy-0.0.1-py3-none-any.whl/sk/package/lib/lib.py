import requests
import pickle
import hashlib
import re
import math
import os
import sys
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup

from datetime import datetime

## host = 'http://account.youongroup.uon'     ## Local
## videoHost = 'http://video.youongroup.uon'  ## Local
host = 'https://accounts-pp.youongroup.com'  ## Production
videoHost = 'https://video-pp.youongroup.com'  ## Production

loginUrl = host + '/auth/login'
chooseAccountUrl = host + '/choose-account'
videosUrl = videoHost + '/1/videos'

# Global Session Handler
s = requests.Session()


def cookie_id(email, password):
    # Generate the cookie hash
    m = hashlib.md5()
    strToHash = (email + password).encode('UTF-8')
    m.update(strToHash)
    checksum = m.hexdigest()
    return checksum


def save_cookie(key):
    with open('storage/' + key, 'wb') as f:
        pickle.dump(s.cookies, f)


def load_cookie(key):
    try:
        with open('storage/' + key, 'rb') as f:
            requestsCookieJar = pickle.load(f)  # Returns a RequestsCookieJar instance
            return requestsCookieJar
    except FileNotFoundError:
        pass


def update_cookie(key, requestsCookieJar):
    s.cookies.update(requestsCookieJar)
    save_cookie(key)


def cookie_is_expired(requestsCookieJar):
    try:
        # cookieId = cookie_id(email, password)
        # requestsCookieJar = load_cookie(cookieId)
        cookie = next(x for x in requestsCookieJar if x.name == 'sts')  # Returns a Cookie instance         

        expires = cookie.expires
        dt_object = datetime.fromtimestamp(expires)

        return cookie.is_expired()
    except Exception as error:
        raise FileNotFoundError


def session_load(email, password):
    try:
        cookieId = cookie_id(email, password)
        cookie = load_cookie(cookieId)
    except Exception as error:
        raise FileNotFoundError


def merge(list1, list2):
    merged_list = [(p1, p2) for idx1, p1 in enumerate(list1)
                   for idx2, p2 in enumerate(list2) if idx1 == idx2]
    return merged_list


def getcsrfToken(soup):
    results = soup.find('meta', attrs={'name': 'csrf-token'})
    csrfToken = results.attrs['content']
    return csrfToken


def login(email, password):
    r1 = s.get(url=loginUrl)

    soup = BeautifulSoup(r1.text, 'lxml')
    csrfToken = getcsrfToken(soup)

    payload = {'email': email, 'password': password, '_token': csrfToken}
    r2 = s.post(url=loginUrl, data=payload)
    return r2


def list_accounts(r):
    soup = BeautifulSoup(r.text, 'lxml')
    csrfToken = getcsrfToken(soup)

    ## TODO List all the accounts and choose one    
    account_names = soup.findAll('input', attrs={'name': 'account_name'})
    account_tokens = soup.findAll('input', attrs={'name': 'account_token'})
    names = [tag.attrs['value'] for tag in account_names]
    tokens = [tag.attrs['value'] for tag in account_tokens]
    merged_list = merge(names, tokens)
    return merged_list


def choose_account(r, token):
    soup = BeautifulSoup(r.text, 'lxml')
    csrfToken = getcsrfToken(soup)

    payload = {'account_token': token, '_token': csrfToken}
    r1 = s.post(url=chooseAccountUrl, data=payload)
    print(r1.text)
    return r1


def get_videos():
    # r1 = s.get(url=videosUrl, cookies=r.cookies)
    r1 = s.get(url=videosUrl)
    print(r1.text)
    return r1


def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def start():
    serviceUrl = 'https://video-pp.youongroup.com/1/upload/bulk'
    # serviceUrl = "http://httpbin.org/post"

    # uploadServiceUrl="http://httpbin.org/post"
    uploadServiceUrl = "https://fast-upload-pp.youongroup.com/upload"

    # TODO Make a POST request to service URL
    r1 = s.get(url='https://video-pp.youongroup.com/')

    soup = BeautifulSoup(r1.text, 'lxml')
    csrfToken = getcsrfToken(soup)

    payload = {
        'shared': False,
        'password': "",
        'end_date': None,
        'max_size': None,
        'directoryId': 1,
        'service': 'ads',
        '_token': csrfToken
    }

    response = s.post(serviceUrl, data=payload)

    if response.status_code == 200:
        code = response.json()['code']

    # filename = "./sample.txt"
    filename = "C:\~\/resources\/videos\/27.mp4"

    # Open file
    f = open(filename, 'rb')

    status = os.stat(filename)
    fileSize = status.st_size

    resumableChunkSize = 2 * 1024 * 1024  ## 25MB chuncksize
    resumableTotalChunks = math.ceil(fileSize / resumableChunkSize)
    print(resumableTotalChunks)
    index = 0
    sizeSum = 0
    offset = 0
    httpOffset = 0

    idAccount = 1
    chunkNumber = 1
    headers = {}

    ## TODO Make a get request to https://upload-pp.youongroup.com/4utzruz5z0
    uploadUrl = "https://upload-pp.youongroup.com/" + code
    response = requests.get(url=uploadUrl)
    soup = BeautifulSoup(response.text, 'lxml')

    # Create a pattern to match names
    # try to match window.maxFileSize = 10737418240;
    # try to match window.maxFiles = 1024;
    # try to match window.jwt = "..."
    # try to match window.fileType = ["mov","avi","mkv","divx","mp4","flv","3gp","3g2","flv","ogv","webm","r3d"];
    name_pattern = re.compile(r'(window.jwt)\ \=\ \"(.*)\"', flags=re.M)
    print(name_pattern)

    # Find all occurrences of the pattern
    names = name_pattern.findall(soup.text)
    jwt = dict(names)['window.jwt']

    for chunk in read_in_chunks(f, resumableChunkSize):
        currentChunkSize = len(chunk)
        sizeSum += len(chunk)
        offset += len(chunk)

        httpOffset = index + len(chunk)
        index = httpOffset

        headers['Authorization'] = 'Bearer ' + jwt
        try:
            payload = {'resumableChunkNumber': chunkNumber,
                       'resumableChunkSize': resumableChunkSize,
                       'resumableCurrentChunkSize': currentChunkSize,
                       'resumableTotalSize': fileSize,
                       'resumableType': 'video',
                       'resumableIdentifier': '4671021-27mp4',
                       'resumableFilename': '%2327.mp4',
                       'resumableRelativePath': '%2327.mp4',
                       'resumableTotalChunks': resumableTotalChunks,
                       'code': '4utzruz5z0',
                       'id': idAccount}

            multipart_form_data = {
                'file': (filename, chunk)
            }

            print(payload)

            r = requests.post(url=uploadServiceUrl, files=multipart_form_data, data=payload, headers=headers)
            ## r = requests.post("http://httpbin.org/post", files=multipart_form_data, data=payload, headers=headers)
            ## print("r: %s, Content-Range: %s" % (r,headers['Content-Range']))
            # pprint(r.json())
            print(r)
            chunkNumber = chunkNumber + 1
        except Exception as e:
            print(e)

    ## f.close()
