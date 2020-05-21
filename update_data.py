import requests as req
import json
import datetime
import pandas as pd
from app.snipets import insert_query
from pathlib import Path
from constants import GIT_API, GIT_FULL_DATA_FOLDER, DATA_FOLDER



Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

normalizedFileNamesList = []
def match_Date(date_string):
    matched = False
    
    try:
        dd = datetime.datetime.strptime(date_string,"%m/%d/%y")
    except Exception as e:
        matched = False
        print('Removendo '+date_string)
        return False
    return dd

def getDataFiles():
    resp = req.get(GIT_API+GIT_FULL_DATA_FOLDER, headers=headers)

    if resp.ok:
        jsonListResp = resp.json()
        if jsonListResp:
            timeSeriesObj = getTimeSeriesObject(jsonListResp)           
            for obj in timeSeriesObj:
                
                download_file(obj)
            if normalizedFileNamesList:
                for eaFile in normalizedFileNamesList:
                  
                    df = pd.read_csv(DATA_FOLDER+'/'+eaFile)
                    _type = checkType(eaFile)
                    insertToDB(df, _type)
def checkType(file_name):
    if 'confirmed' in file_name:
        return 'casos'
    if 'recovered' in file_name:
        return 'recuperados'
    if 'deaths' in file_name:
        return 'mortes'          
    return False

def download_file(obj):
    with req.get(obj['download_url'], stream = True) as response:
        with open(DATA_FOLDER+'/'+obj['name'], 'wb') as f:
            for chunk in response.iter_content(chunk_size = 1024):
                f.write(chunk)
            normalizeData(obj['name'])

def insertToDB(df,_type):
    for i, row in df.iterrows():
        pais = ""
        for idx, val in enumerate(row):
            data = ""
            if "Country" in  row.index[idx]:
                pais = val
            else:
                data = row.index[idx]

            if (data == ""):
                continue
            if type(val) == float:
                val = int(val)
            data = match_Date(data)
            print (data)
            insert_query(quantidade=val,data=data, nome_pais=pais, _type=_type)
def normalizeData(csvName):
    df = pd.read_csv(DATA_FOLDER+'/'+csvName)
    df = df.drop(df.columns[[0]], axis=1) 
    grouped = df.groupby(by=["Country/Region"])
    column = [column for column in df.columns if match_Date(column)]
    result = grouped[column].agg('sum')
    filename = 'normalized_'+csvName
    result.to_csv(DATA_FOLDER+'/'+filename)
    normalizedFileNamesList.append(filename)

def getTimeSeriesObject(filesList):
    timeSeriesObj = []
    for file in filesList:
        if ('time_series' and 'global') in file['name']:
            timeSeriesObj.append(file)
    return timeSeriesObj
    
if __name__ == "__main__":
    getDataFiles()


