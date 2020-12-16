# Bibliotecas
import time
import os
import re
import datetime
import pandas as pd


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException      

# Ler JSON
json = pd.read_json('cargo.json', dtype=str)

# Pegar cargo e cidade
json_cargo = json['Cargo'][0]
json_cidade = json['Cargo'][1]

# Caminho atual
path = os.getcwd()

# Verificar se pasta Repositorio existe
if os.path.isdir('EmpregosCom') == False:
    print('A pasta "EmpregosCom" não existe. Criando diretório.')
    os.mkdir('EmpregosCom')
else:
    print('A pasta "EmpregosCom" existe.')

driver = webdriver.Chrome()
driver.get('https://www.empregos.com.br/')

# Preencher os campos vagas e local
vaga = driver.find_element_by_css_selector('#ctl00_ContentBody_ucSuggestCargo_txtCargo').is_enabled()
vaga = driver.find_element_by_css_selector('#ctl00_ContentBody_ucSuggestCargo_txtCargo').click()
vaga = driver.find_element_by_css_selector('#ctl00_ContentBody_ucSuggestCargo_txtCargo').send_keys(json_cargo)

cidade = driver.find_element_by_css_selector('#ctl00_ContentBody_ucSuggestCidade_txtCidade').click()
cidade = driver.find_element_by_css_selector('#ctl00_ContentBody_ucSuggestCidade_txtCidade').send_keys(json_cidade)


lupa = driver.find_element_by_css_selector('#ctl00_ContentBody_lnkBuscar').click()
time.sleep(1)


qntd_vagas = driver.find_elements_by_xpath('//*[@id="ctl00_ContentBody_divPaiMioloBusca"]/ul/li')

vagas = []
link = []
salarios = []
local = []
publicacao = []
resumo = []

for j in range(1, len(qntd_vagas)):
          try:
                    vagas.append(driver.find_element_by_css_selector(f'#ctl00_ContentBody_divPaiMioloBusca > ul > li:nth-child({j}) > div.grid-13-16.col-esquerda > div.descricao.grid-12-16 > h2 > a').text)
                    link.append(driver.find_element_by_css_selector(f'#ctl00_ContentBody_divPaiMioloBusca > ul > li:nth-child({j}) > div.grid-13-16.col-esquerda > div.descricao.grid-12-16 > h2 > a').get_attribute('href'))
                    salarios.append(driver.find_element_by_css_selector(f'#ctl00_ContentBody_divPaiMioloBusca > ul > li:nth-child({j}) > div.grid-3-16.col-direita > div > div:nth-child(3)').text)
                    local.append(driver.find_element_by_css_selector(f'#ctl00_ContentBody_divPaiMioloBusca > ul > li:nth-child({j}) > div.grid-13-16.col-esquerda > div.descricao.grid-12-16 > h3').text)
                    publicacao.append(driver.find_element_by_css_selector(f'#ctl00_ContentBody_divPaiMioloBusca > ul > li:nth-child({j}) > div.grid-13-16.col-esquerda > div.descricao.grid-12-16 > h3').text)
                    resumo.append(driver.find_element_by_css_selector(f'#ctl00_ContentBody_divPaiMioloBusca > ul > li:nth-child({j}) > div.grid-13-16.col-esquerda > div.descricao.grid-12-16 > p.resumo-vaga').text)
          except :
                    pass

driver.close()

df = pd.DataFrame([vagas, link, salarios, local, publicacao, resumo])
df = df.T
df.columns = ['VAGAS',  'LINKS', 'SALARIOS', 'LOCAL', 'LOCAL DA PUBLICACAO', 'RESUMO DA VAGA']

df.to_csv(path + '\EmpregosCom\EmpregosCom.csv', sep=';', encoding='utf-8')