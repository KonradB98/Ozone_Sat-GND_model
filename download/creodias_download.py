import requests
import json
from tqdm import tqdm
import re
import sys
import download.creodias_credentials as cc
import os
import zipfile
import pathlib

PDP = pathlib.Path(__file__).parents[0]
SAT_PATH = PDP.joinpath('data/Lisbon/sat/')

"""
Script borrowed from below url:
https://creodias.eu/forum/-/message_boards/message/154531
"""

finder_api_url = '''https://finder.creodias.eu/resto/api/collections/Sentinel5P/search.json?maxRecords=10&startDate=2022-03-31T00%3A00%3A00Z&completionDate=2022-03-31T23%3A59%3A59Z&processingLevel=LEVEL2&productType=L2__O3____&timeliness=Offline&geometry=POLYGON((-9.5361328125+37.79242240798855%2C-7.789306640625+37.79242240798855%2C-7.789306640625+39.55911824217185%2C-9.5361328125+39.55911824217185%2C-9.5361328125+37.79242240798855))&sortParam=startDate&sortOrder=descending&status=all&dataset=ESA-DATASET'''

def get_keycloak_token():
    h = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    d = {
    'client_id': 'CLOUDFERRO_PUBLIC',
    'password': cc.password,
    'username': cc.username,
    'grant_type': 'password'
    }
    resp = requests.post('https://auth.creodias.eu/auth/realms/dias/protocol/openid-connect/token', data=d, headers=h)
    # print(resp.status_code)
    try:
        token = json.loads(resp.content.decode('utf-8'))['access_token']
    except KeyError:
        print("Can't obtain a token (check username/password), exiting.")
        sys.exit()
    # print(token)
    return token

def creodiasDownload():
    response = requests.get(finder_api_url)
    for feature in json.loads(response.content.decode('utf-8'))['features']:
        token = get_keycloak_token()
        download_url = feature['properties']['services']['download']['url']
        download_url = download_url + '?token=' + token
        total_size = feature['properties']['services']['download']['size']
        title = feature['properties']['title']
        filename = title + '.zip'
        r = requests.get(download_url, stream=True)
        if "Content-Disposition" in r.headers.keys():
            filename = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0))
        if total_size <= 100:
            print(r.text)
            sys.exit("Please try again in few moments.")
        block_size = 1024 #1 Kibibyte
        print('downloading:', filename)
        t=tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(filename, 'wb') as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            print("ERROR, something went wrong")
        """
        Unziping dir, take only NC file and remove zip folder
        """
        # ncFile = title + '/' + title + '.nc'
        ncFile = title + '/' + title + '.nc'
        with zipfile.ZipFile(filename) as z:
            with open(SAT_PATH.joinpath(title+'.nc'), 'wb') as f:
                f.write(z.read(ncFile))
                f.close()
            z.close()
        os.remove(filename)

if __name__ == "__main__":
    creodiasDownload()




