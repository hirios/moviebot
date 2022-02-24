import os
import requests
from color import Color
from bs4 import BeautifulSoup
import re


color = Color()


with open('catalogo/filmes.txt', 'r', encoding='utf-8') as file:
    filmes = file.readlines()


with open('catalogo/series.txt', 'r', encoding='utf-8') as file:
    series = file.readlines()


def search_filmes(movie_name):
    """ 
    Essa função retorna uma tupla contendo uma string e um dicionário.
    A string contém os nomes dos filmes.
    O dicionário contém os links dos filmes, estes na mesma ordem que os nomes. 
    """

    movie_name = movie_name.lower().strip()
    cont = 1
    names = ""
    links = []

    # "filmes" É UMA VARIÁVEL CONTENDO A LISTA DE FILMES
    # EXEMPLO: Harry Potter || /video/harry_potter.html
    for x in filmes:
        if movie_name in x.lower():
            names += str([cont]) + " " + x.strip().split('||')[0] + "\n\n"
            cont += 1 
            links.append(x.strip().split("||")[1])

    return names, links


def search_series(serie_name):
    """ 
    Essa função retorna uma tupla contendo uma string e um dicionário.
    A string contém os nomes das series.
    O dicionário contém os links das series, estes na mesma ordem que os nomes. 
    """

    serie_name = serie_name.lower().strip()
    cont = 1
    names = ""
    links = []

    # "series" É UMA VARIÁVEL CONTENDO A LISTA DE SÉRIES
    # EXEMPLO: Arrow || /video/arrow_3temporada.html
    for x in series: 
        if serie_name in x.lower():
            names += str([cont]) + " " + x.strip().split('||')[0] + "\n\n"
            cont += 1 
            links.append(x.strip().split("||")[1])

    return names, links


headers = {"authority": "dietafitness.fun",
"method": "GET",
"path": "/player3/serverf3.php?vid=AVDAEBLA",
"cookie": "__dtsu=10401591100498D1D090A5E25D83E1B0",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
"referer": "https://hlb.dietafitness.fun/instagram/campanha.php?data=/player3/server14hlb.php?vid=ASMNSPRPDRST01EP01&rc=1"}


def get_filename(complemento):
    return rede(complemento)


def get_episodes(rota):
    """
    A função "get_episodes" retorna uma tupla com dois dicionários (dublado, legendado).
    Os dicionários contêm as rotas de cada episódio da série.
    Rota do site relativa à série, exemplo => '/watch.php?vid=9e33db9a8'  """

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "http://redecanais.wf",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Mobile Safari/537.36"}

    try:
        html = requests.get('https://redecanais.wf' + f'{rota}',timeout=15, headers=headers).text
    except:
        print('!!! Erro na REQUISIÇÃO de uma série !!!')
    html_parsed = BeautifulSoup(html, 'html.parser')
    html_div_links = html_parsed.find_all("div", {"class": "pm-category-description"})
    html_links = html_div_links[0].find_all(href=True)


    dublado = []
    legendado = []
    for x in html_links:
        if (x.text).strip() == "Dublado" or x.text == "dublado" or x.text == "Assistir" or  x.text == "assistir":
            dublado.append(x['href'])
        elif (x.text).strip() == "Legendado" or x.text == "legendado":
            legendado.append(x['href'])
        else:
            print('Erro ao verificar linguagem')
    
    return dublado, legendado


def rede(complemento):
    html = requests.get("https://redecanais.wf" + complemento)
    path = [x for x in html.text.split('"') if "/server" in x ][0]
    print(color.cg("Path:"), path)

    filename = re.search("vid=.+?(&|$|'|])", str(path)).group(0)
    if filename[-1] == '&':
        filename = filename[:-1].split("=")[1]

    elif filename[-1] == "'":
        filename = filename[:-1].split("=")[1]

    elif filename[0:4] == "vid=":
        filename = filename.split('vid=')[-1]
    else:
        filename = filename.split("=")[1]
    print(color.cg("Filename:"), filename)

    pre_player = [x for x in html.text.split('"') if filename in x][0]
    page_pre_player = requests.get("https://dietafitness.fun" + pre_player, headers=headers)
    
    player = [x for x in page_pre_player.text.split('"') if filename in x][-1]
    page_player = requests.get("https://dietafitness.fun" + player, headers=headers)
    
    redirect = [x for x in page_player.text.split('"') if filename in x][0]

    html_redirect = requests.get(redirect).text
    link = [x for x in html_redirect.split('"') if "http" in x][-1].split("'")[-2]
    print(color.cg("Movie Link:"), link)

    return str(link)
