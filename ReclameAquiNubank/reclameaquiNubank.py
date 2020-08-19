#Bibliotecas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

import time
import json 
import requests
import pandas as pd
import glob
from pathlib import Path
import os

#Pre-Requisitos do Firefox
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

binary = FirefoxBinary('C:\\Users\\felipesa\\AppData\\Local\\Mozilla Firefox\\firefox.exe')

#Browser-Robo
web = webdriver.Firefox(firefox_binary=binary, executable_path='geckodriver.exe', capabilities=firefox_capabilities)
#web = webdriver.PhantomJS()
web.get('https://www.reclameaqui.com.br/empresa/nubank/lista-reclamacoes/')

bs = BeautifulSoup(web.page_source, 'html')

#Selecionar Todas Reclamacoes. Isso gera o json 
todas_reclamacoes = web.find_element_by_css_selector('li.active:nth-child(1)')
todas_reclamacoes.click()


page = requests.get('https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/0?company=88850')
df_json = pd.read_json('https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/0?company=88850')
df_json.to_json(f'page0.json',index=True)


#Laco para pegar os dados
for i in range(1,10):
    prox_pag = web.find_element_by_css_selector('.pagination-next > a:nth-child(1)')
    prox_pag.click()
    time.sleep(2)
    #Acessar a pag que contem os dados 
    page = requests.get(f'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/{i}0?company=88850')
    time.sleep(2)
    #Transformar pag. em JSONs
    df_json = pd.read_json(f'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/{i}0?company=88850')

    df_json.to_json(f'page{i}.json',index=True)


#Juntar os JSONs
df_final = []
for f in glob.glob("*.json"):
    with open(f, "rb") as infile:
        df_final.append(json.load(infile))

#Pegar as informacoes dos json
titulos =[]
infos =[]
locais =[]
datas = []

for i in range(10):
    for j in range(10):
        titulo = df_final[i]['complainResult']['complains']['data'][j]["title"]
        titulos.append(titulo)    
        info = df_final[i]['complainResult']['complains']['data'][j]["description"]
        infos.append(info)
        local = df_final[i]["complainResult"]["complains"]["data"][j]["userCity"]
        locais.append(local)
        data = df_final[i]["complainResult"]["complains"]["data"][j]["created"]
        datas.append(data)


#Criacao do Dataframe
data_frame = [titulos, infos, locais, datas]
data_frame = pd.DataFrame(data_frame)
data_frame = data_frame.T


#Salvar o DF
data_frame.reset_index().to_csv('df.csv', index=False, header=False, sep=';', encoding='latin1')
