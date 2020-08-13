#Bibliotecas
import os

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import time
import json 
from bs4 import BeautifulSoup

#Pre-Requisitos do Firefox
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

binary = FirefoxBinary('C:\\Users\\felipesa\\AppData\\Local\\Mozilla Firefox\\firefox.exe')

#Browser-Robo
web = webdriver.Firefox(firefox_binary=binary, executable_path='geckodriver.exe', capabilities=firefox_capabilities)
#web = webdriver.PhantomJS()
web.get() #----------------> Coloque aqui o site que deseja fazer o scraping

#Caixa de localizacao
time.sleep(4)
campo_notificacoes = web.find_element_by_class_name('shoppush-prompt-btn.shoppush-disallow-btn')
campo_notificacoes.send_keys('Agora não')

#Campos para serem preenchidos
campo_nome = web.find_element_by_id('PSWidgets_wt1_block_wt12_wtMainContent_wt3_wt40_wtInscricaoLead_Nome') #Campo Nome
time.sleep(1) 
campo_nome.send_keys('Felipe Azevedo')
campo_telefone = web.find_element_by_id('PSWidgets_wt1_block_wt12_wtMainContent_wt3_wt40_wtInscricaoLead_Telefone') #Campo Telefone
time.sleep(1) 
campo_telefone.send_keys('32988154477')
campo_email = web.find_element_by_id('PSWidgets_wt1_block_wt12_wtMainContent_wt3_wt40_wtInscricaoLead_Email') #Campo email
time.sleep(1) 
campo_email.send_keys('felipeazevedo@gmail.com')
check_info_email = web.find_element_by_id('PSWidgets_wt1_block_wt12_wtMainContent_wt3_wt40_wtInscricaoLead_AceiteNewsletter') #Tickar o box do info por email
time.sleep(2)
check_info_email.click()
time.sleep(1) 
check_info_sms = web.find_element_by_id('PSWidgets_wt1_block_wt12_wtMainContent_wt3_wt40_wtInscricaoLead_AceiteSMS') #Tickar o box do info por sms
time.sleep(2)
check_info_sms.click()
time.sleep(2) 
check_info_sms = web.find_element_by_id('PSWidgets_wt1_block_wt12_wtMainContent_wt3_wt40_SilkUIFramework_wt42_block_wtActionsRight_wt49') #Botao Prosseguir
time.sleep(1)
check_info_sms.click()
time.sleep(5)


#pegar os dados com bs4
bs = BeautifulSoup(web.page_source, 'html')

nome_curso = []
camp = [] # Lista para o campus
per = [] # Lista para os periodos
prec = [] # lista para os preços

#Nome do cuso
for n_campus in bs.select('a[id="PSWidgets_wt1_block_wt12_wtMainContent_wt3_SilkUIFramework_wtWizard_block_wt9_wtWizardParent_wt11_wtStep_wtStep2_wt49"]'):
    print('Nome do Curso: {}'.format(n_campus.get_text()))
    nome_curso.append('Nome do Curso: {}'.format(n_campus.get_text()))
time.sleep(0.5)

#Encontrando os campi
for campus in bs.select('div[class="title_list"]'):
    print('Campus: {}'.format(campus.get_text()))
    camp.append('Campus: {}'.format(campus.get_text()))
time.sleep(1)

#Encontrando os periodos
for periodo in bs.select('span[class="Bold"]'):
    if periodo.get_text() != "Inscrições" and periodo.get_text() != "Crédito Estudantil":
        print('Perido: {}'.format(periodo.get_text()))
        per.append('Perido: {}'.format(periodo.get_text()))
time.sleep(1)

#Encontrando os preços
for preco in bs.select('span[class="valorPor Bold Text_NoWrap Flagged"]'):
    if preco.get_text() != "R$99,00" and preco.get_text() != "R$69,00" and preco.get_text() != "R$49,90":
        print(preco.get_text())
        prec.append('preco: {}'.format(preco.get_text()))


#Dados
dic = {
    'Nome do curso': nome_curso,
    'Campus': camp,
    'Periodo': per,
    'Preco': prec
}


out_file = open("preco_info.json", "a", encoding='utf-8')  
    
json.dump(dic, out_file, indent = 6, ensure_ascii=False)  
out_file.close()  

#Fechar a janela
web.close()
