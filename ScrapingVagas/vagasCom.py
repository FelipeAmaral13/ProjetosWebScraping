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

json_cargo = json['Cargo'][0]


# Caminho atual
path = os.getcwd()

# Verificar se pasta Repositorio existe
if os.path.isdir('VagasCom') == False:
    print('A pasta "VagasCom" não existe. Criando diretório.')
    os.mkdir('VagasCom')
else:
    print('A pasta "VagasCom" existe.')

driver = webdriver.Chrome()
driver.get('https://www.vagas.com.br/')

# Instanciar a classe que irá esperar até 5 segundos
wait = WebDriverWait(driver, 5)

cargo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#nova-home-search')))
cargo = driver.find_element_by_css_selector('#nova-home-search').click()
cargo = driver.find_element_by_css_selector('#nova-home-search').send_keys(json_cargo)

busca = driver.find_element_by_css_selector('#header > div.nova-home-header > div.nova-home-search-container > div > div.search-field > i').click()

time.sleep(1)
vagas1 = driver.find_elements_by_xpath('//*[@id="todasVagas"]/ul/li')

vaga = []
resumo = []
empresa = []
local = []
data = []
link = []

for i in range(1, len(vagas1)):
    vaga.append(driver.find_element_by_xpath('//div[@class="informacoes-header"]/h2/a/mark').text)
    resumo.append(driver.find_element_by_xpath(f'//*[@id="todasVagas"]/ul/li[{i}]/div/p').text)
    empresa.append(driver.find_element_by_xpath(f'//*[@id="todasVagas"]/ul/li[{i}]/header/div[2]/span').text)
    local.append(driver.find_element_by_xpath(f'//*[@id="todasVagas"]/ul/li[{i}]/footer/span[1]').text)
    try:
        data.append(driver.find_element_by_xpath(f'//*[@id="todasVagas"]/ul/li[{i}]/footer/span[2]').text)
    except :
        data.append(driver.find_element_by_xpath(f'//*[@id="todasVagas"]/ul/li[{i}]/footer/span').text)
    link.append(driver.find_element_by_xpath(f'//*[@id="todasVagas"]/ul/li[{i}]/header/div[2]/h2/a').get_attribute('href'))

driver.close()


# Criacao do dataframe
df = [vaga, resumo, empresa, local, data, link]
df = df.T
df = pd.DataFrame(df)

df.to_csv(path + '\\VagasCom\\VagasCom.csv', sep=';', encoding='utf-8')