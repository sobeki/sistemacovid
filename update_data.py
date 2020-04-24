import requests as req
import json
from pathlib import Path
from constants import GIT_API, GIT_FULL_DATA_FOLDER, DATA_FOLDER



Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def getDataFiles():
    resp = req.get(GIT_API+GIT_FULL_DATA_FOLDER, headers=headers)

    if resp.ok:
        jsonListResp = resp.json()

        if jsonListResp:
            timeSeriesObj = getTimeSeriesObject(jsonListResp)
            
            for obj in timeSeriesObj:
                download_file(obj)

def download_file(obj):
    with req.get(obj['download_url'], stream = True) as response:
        with open(DATA_FOLDER+'/'+obj['name'], 'wb') as f:
            for chunk in response.iter_content(chunk_size = 1024):
                f.write(chunk)

def getTimeSeriesObject(filesList):
    downloadUrls = []
    for file in filesList:
        if ('time_series' and 'global') in file['name']:
            downloadUrls.append(file)
    return downloadUrls
getDataFiles()