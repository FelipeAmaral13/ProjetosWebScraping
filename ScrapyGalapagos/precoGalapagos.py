import requests
import pandas as pd

url = requests.get('https://www.galapagosjogos.com.br/ccstoreui/v1/products?totalResults=true&totalExpandedResults=true&catalogId=3&limit=84&offset=0&categoryId=B2C-Promocoes&includeChildren=true&storePriceListGroupId=vBRLPriceGroup')
page = url.json()

#Nome do produto
nomes = []
for n in range(84):
    print(page['items'][n]['primaryImageAltText'])
    nomes.append(page['items'][n]['primaryImageAltText'])

#Preco de Original
precos_original = []
for po in range(84):
    print(page['items'][po]['x_precoSugeridoDeVenda'])
    precos_original.append(page['items'][po]['x_precoSugeridoDeVenda'])

#Preco de oferta
precos_oferta = []
for p in range(84):
    print(page['items'][p]['salePrice'])
    precos_oferta.append(page['items'][p]['salePrice'])

#Info dos jogos
infos = []
for info in range(84):
    print(page['items'][info]['x_informacoes'])
    infos.append(page['items'][info]['x_informacoes'])

#Tempo de jogo
tempo = []
for temp in range(84):
    print(page['items'][temp]['x_tempoDePartida'])
    tempo.append(page['items'][temp]['x_tempoDePartida'])


#Juntar em um lista
data = [nomes, precos_original, precos_oferta, infos, tempo]

#Criacao do Dataframe
df = pd.DataFrame(data)
df = df.T
df.columns = ['Nome do Jogo', 'Preco Original', 'Preco Promocional', 'Informacoes', 'Tempo Medio de Jogo']

df = df.to_csv('BD_Jogos_Galapagos.csv', index=False, sep=';', encoding='latin1' )