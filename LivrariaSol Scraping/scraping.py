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

# Caminho atual
path = os.getcwd()

# Verificar se pasta Repositorio existe
if os.path.isdir('LivrariaPrecos') == False:
    print('A pasta "LivrariaPrecos" não existe. Criando diretório.')
    os.mkdir('LivrariaPrecos')
else:
    print('A pasta "LivrariaPrecos" existe.')

driver = webdriver.Chrome()
driver.get('https://www.livrariasol.com.br/didatico')

pag = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div[1]').text

qntd_pag = int(pag[29])

nome = []
preco = []
qtd_parcelas = []

for k in range(qntd_pag):

          total_livros = driver.find_elements_by_class_name('product')

          for i in range(len(total_livros)):
                    
                            nome.append(driver.find_element_by_xpath(f'/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/div/div/div[{i+1}]/article/div[2]/h1/a').text)
                            time.sleep(0.5)
                            try:
                                preco.append(driver.find_element_by_xpath(f'/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/div/div/div[{i+1}]/article/div[2]/div/div[1]/div/div/span[2]').text)
                                time.sleep(0.5)
                            except:
                                preco.append(driver.find_element_by_xpath(f'/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/div/div/div[{i+1}]/article/div[2]/div/div[1]/div/div/span[2]').text)
                                time.sleep(0.5)
                            try:
                                qtd_parcelas.append(driver.find_element_by_xpath(f'/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/div/div/div[{i+1}]/article/div[2]/div/div[2]/span[5]/span/span/strong').text)
                                time.sleep(0.5)
                            except:
                                qtd_parcelas.append(driver.find_element_by_xpath(f'/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/div/div/div[{i+1}]/article/div[2]/div/div[2]/span[5]/span/strong').text)
                                time.sleep(0.5)

          try:                                                            
                    next_pag = driver.find_element_by_css_selector('body > div.wrapper > div > main > div > div > div.page-catalog__container > div.page-catalog__content > div.page-catalog__toolbar.page-catalog__toolbar--top > div > div > div.toolbar__paginate > div > div > div.paginate__pages > span.paginate__link.paginate__link--next > a').is_enabled()
                    next_pag = driver.find_element_by_css_selector('body > div.wrapper > div > main > div > div > div.page-catalog__container > div.page-catalog__content > div.page-catalog__toolbar.page-catalog__toolbar--top > div > div > div.toolbar__paginate > div > div > div.paginate__pages > span.paginate__link.paginate__link--next > a').click()

          except :
                    print('Acabou!')


df = pd.DataFrame([nome, preco])
df = df.T
df.columns = ['Nome', 'Preço']
df.to_csv('solLivraria.csv', sep=';', encoding='latin1')