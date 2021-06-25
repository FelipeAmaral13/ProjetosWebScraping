#!C:\Users\felipesa\AppData\Local\Programs\Python\Python38\python3.exe


#################################################################
#                                                               #
#                           Bibliotecas                         #
#                                                               #
#################################################################

import time
import os
import re
import datetime
import pandas as pd
import sys
from pathlib import Path
import numpy as np

from calendar import monthrange


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException



#################################################################
#                                                               #
#              Verificar se pasta Repositorio existe            #
#                                                               #
#################################################################

# Caminho atual
path = os.getcwd()

#Data de hoje
hoje = datetime.date.today()
# Mes atual
mes = hoje.month

# Ano atual
ano = hoje.year

# Mes passsado
mes_passado = mes - 1

# Se o mes atual for Janeiro é preciso pegar dezembro do ano passado
if mes == 1:
    ano = ano -1

mes_curr, dias_curr = monthrange(ano, mes_passado)

dias_ = np.arange(1, dias_curr+1)

# Configuracoes basicas do robo
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('headless')


# Driver do robo

driver = webdriver.Chrome(executable_path = str(Path(path).parents[0]) +  r'\chromedriver.exe', chrome_options=chrome_options)
driver.get('https://www.bcb.gov.br/')

# Instanciar a classe que irá esperar até 5 segundos
wait = WebDriverWait(driver, 15)

# Scroll da tela
driver.execute_script("window.scrollTo(0, 500)") 


# Clicando "Ver todas as moedas"
try:
    modedas = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div/conversormoedas/div[2]/a')))
    time.sleep(1)
    modedas = driver.find_element_by_xpath('//*[@id="home"]/div/div[1]/div[2]/div/conversormoedas/div[2]/a').click()

except (WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException)  as e :
    driver.quit()
    sys.exit("Error message")

# Clicar no icone das setas
setas = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[2]/div[3]/div/button')))
setas = driver.find_element_by_xpath('/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[2]/div[3]/div/button').click()

conv = []
for i in range(len(dias_))[:10]:
    print(dias_[i])

    # Selecionar datas
    try:

        sel_datas = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[1]/div/input[2]')))
        #Apagar a data presente
        apagar_data = driver.find_element_by_name('inputDate').send_keys(Keys.CONTROL, 'a')
        apagar_data = driver.find_element_by_name('inputDate').send_keys(Keys.BACKSPACE)


        enviar_data = driver.find_element_by_name('inputDate').send_keys(int(dias_[i]))
        enviar_mes = driver.find_element_by_name('inputDate').send_keys(mes_curr)
        enviar_ano = driver.find_element_by_name('inputDate').send_keys(ano)

        apagar_data = driver.find_element_by_name('inputDate').send_keys(Keys.ENTER)


        time.sleep(2)

        # Clicar no icone das setas
        #setas = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[2]/div[3]/div/button')))
        #setas = driver.find_element_by_xpath('/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[2]/div[3]/div/button').click()
        #setas = driver.find_element_by_xpath('/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[2]/div[3]/div/button').click()
        #time.sleep(0.5)

        # Pegar a conversao
        conversao = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[2]/div/div[1]/div[2]/div')))
        conversao = driver.find_element_by_xpath('/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[2]/div/div[1]/div[2]/div')
        enviar_ano = driver.find_element_by_name('inputDate').send_keys(ano)
        conversa_total = re.search(r"conversão: (\d+,\d+)?", conversao.text).group(1)  # Nome do aluno
        conv.append([str(int(dias_[i]))+ '/' + str(mes_curr)+ '/' + str(ano), conversa_total])

        # clicar no 'reload'
        reload = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[2]/div[5]/div/button')))
        reload = driver.find_element_by_xpath('/html/body/app-root/app-root/main/dynamic-comp/div/bcb-pagina-tipo0/div/bcb-pagina-tipo4/div[2]/div/dynamic-comp/div/div/bcb-detalhesconversor/div/div[1]/form/div[2]/div[5]/div/button').click()

    except (WebDriverException, NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException)  as e :
        driver.quit()
        sys.exit("Error message")

driver.close()

# Lista de datas e valores
datas = [conv[i][0] for i in range(len(conv))]
valores = [conv[i][1] for i in range(len(conv))]

# Dataframe das Datas e Valores
df = pd.DataFrame(list(zip(datas,valores)), columns=['DATAS', 'VALORES'])

val_min = df['VALORES'].min()
val_max = df['VALORES'].max()

print(f'O valor min é: {val_min}, valor max é: {val_max}')

df.to_csv('Valores.csv', sep=';', encoding='latin1')


