import os
import requests
from bs4 import BeautifulSoup


lista = """
/browse-numerosesimbolos-series-videos-1-date.html
/browse-letra-a-series-videos-1-date.html
/browse-letra-b-series-videos-1-date.html
/browse-letra-c-series-videos-1-date.html
/browse-letra-d-series-videos-1-date.html
/browse-letra-e-series-videos-1-date.html
/browse-letra-f-series-videos-1-date.html
/browse-letra-g-series-videos-1-date.html
/browse-letra-h-series-videos-1-date.html
/browse-letra-i-series-videos-1-date.html
/browse-letra-j-series-videos-1-date.html
/browse-letra-k-series-videos-1-date.html
/browse-letra-l-series-videos-1-date.html
/browse-letra-m-series-videos-1-date.html
/browse-letra-n-series-videos-1-date.html
/browse-letra-o-series-videos-1-date.html
/browse-letra-p-series-videos-1-date.html
/browse-letra-q-series-videos-1-date.html
/browse-letra-r-series-videos-1-date.html
/browse-letra-s-series-videos-1-date.html
/browse-letra-t-series-videos-1-date.html
/browse-letra-u-series-videos-1-date.html
/browse-letra-v-series-videos-1-date.html
/browse-letra-w-series-videos-1-date.html
/browse-letra-x-series-videos-1-date.html
/browse-letra-y-series-videos-1-date.html
/browse-letra-z-series-videos-1-date.html
""".split()

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Cache-Control": "no-cache",
"Connection": "keep-alive",
"Pragma": "no-cache",
"Referer": "http://redecanais.wf",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36"}


def link_series(url):
    try:
        var = requests.get("https://redecanais.se" + f'{url}', timeout=30, headers=headers).text
    except Exception as err:
        print(x, f'OUTRO ERRO OCORREU: {err}')

    soup = BeautifulSoup(var, 'html.parser')
    soup = soup.find_all("ul", {"class": "list-inline"})[1]   
    titulos_html = soup.find_all('a')
    complementos = [x['href'] for x in titulos_html]
    titulos = [x.text for x in titulos_html]
    return complementos, titulos


complementos_finais = []
titulos_finais = []

for url in lista:
    dual = link_series(url)
    complementos_finais += dual[0]
    titulos_finais += dual[1]

with open('series.txt', 'a', encoding="utf-8") as file:
    for x in range(0, len(titulos_finais)):
        file.write(titulos_finais[x] + "||" + complementos_finais[x] + "\n")


def get_episodes(complemento):
    var = requests.get('https://redecanais.se" + f{complemento}').text
    soup = BeautifulSoup(var, 'html.parser')
    soup.find_all("div", {"class": "pm-category-description"})
    href = teste[0].find_all(href=True)

    dublado = []
    legendado = []
    for x in href:
        if (x.text).strip() == "Dublado" or x.text == "dublado":
            dublado.append(x['href'])
        elif (x.text).strip() == "Legendado" or x.text == "legendado":
            legendado.append(x['href'])
        else:
            print('Erro ao verificar linguagem')

    print(dublado)
            
