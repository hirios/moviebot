import requests
from bs4 import BeautifulSoup
from color import Color


color = Color()
titulos = []
links = []

for c in range(1, 867):
    try:
        html = requests.get(f"https://redecanais.wf/browse-filmes-videos-{c}-date.html", timeout=10)
    except Exception as e:
        print(color.cr("[ERRO]: "), "Erro no request das paginas dos filmes")
        print(color.cr("[ERRO]: "), e)
        quit()

    if html.status_code == 200:
        print(color.cg("[STATUS]:"), 200)
        try:
            soup = BeautifulSoup(html.text, 'html.parser')
            titulos += [x.text.split("\n")[1] for x in soup.find_all("div", {"class": "caption"})]
            links += [x.a.get("href") for x in soup.find_all("div", {"class": "caption"})]

        except Exception as e:
            print(color.cr("[ERRO]: "), "Erro ao raspar lista de filmes")
            print(color.cr("[ERRO]: "), e)
            quit()
    else:
        print(color.cr("[STATUS]:"), html.status_code)
        

with open('filmes.txt', 'a', encoding="utf-8") as file:
    for c in range(0, len(titulos)):
        file.write(titulos[c] + "||" + links[c] + "\n")
