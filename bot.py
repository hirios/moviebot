import os
import time
import requests
import telepot
from color import Color
from pprint import pprint
#from player import Player
#from vlc import start_stream
from bs4 import BeautifulSoup
from file_name import *
import re


color = Color()


def dividir(string):
    string = string
    lista = []
    for i, char in enumerate(string):
        if "\n" in char:
            lista.append(i + 1)
    num = int(len(lista) / 2)
    num = lista[num]
    return num


ids = {}
ids = ids.copy()
ids_series = {}
ids_series = ids_series.copy()


def filmes(texto, msg):
    global ids, ids_series, bot

    try:
        if ids[msg['chat']['id']]:
            del ids[msg['chat']['id']]
    except KeyError:
        pass
    except:
        pass

    # if já tiver pesquisa nas séries, delete    
    try:
        if ids_series[msg['chat']['id']]:
            del ids_series[msg['chat']['id']]
    except KeyError:
        pass
    except:
        pass

    msg = msg
    # Se o id já tiver uma busca, é sobreescrito no dicionário sobre o id dele  Linha: 24       
    try:
        movie = re.split("(F:|f:)", texto)[1]
    except:
        movie = texto[1:].strip()

    busca = search_filmes(movie)
    if len(busca[0]) == 0:
        bot.sendMessage(msg['chat']['id'], "Filme não encontrado!")
    # else:
    #     num = dividir(busca[0])
    ######
    bot.sendMessage(msg['chat']['id'], busca[0])
    #bot.sendMessage(msg['chat']['id'], busca[0][num:])
    ids.update({msg['chat']['id']: busca[1]})
    #print(ids)
    #print('Resposta enviada para', msg['chat']['id'], "\n")


def filmes_ID(msg):
    global ids, ids_series, bot
    
    msg = msg
    if msg['chat']['id'] in ids:
        try:
            numero = int(msg['text'])
        except:
            bot.sendMessage(msg['chat']['id'], 'Digite um número válido')

        bot.sendMessage(msg['chat']['id'], "Tentando conexão...\nEm caso de erro, tente novamente!")
        complemento = ids[msg['chat']['id']][numero - 1]
        url_final = get_filename(complemento)

        # url_final = get_stream_filme(filename).strip()
        # url_final2 = "https://www.radiantmediaplayer.com/test-your-streaming-url.html?streamProtocol=mp4&streamUrl=%20" + url_final.replace("https://", r"https%3A%2F%2F").replace("/", r"%2F").replace("?", r"%3F").replace("=", r"%3D")
        bot.sendMessage(msg['chat']['id'], url_final)
        # start_stream(url_final)
        #Player(url_final)

    
def series(texto, msg):
    global ids, ids_series, bot

    # Se for uma série, deleta id em ids de filmes
    try:
        if ids[msg['chat']['id']]:
            del ids[msg['chat']['id']]
    except KeyError:
        pass
    except:
        pass

    # if já tiver pesquisa nas séries, delete    
    try:
        if ids_series[msg['chat']['id']]:
            del ids_series[msg['chat']['id']]
    except KeyError:
        pass
    except:
        pass

    # Tenta separar por "f"    
    try:
        serie = re.split("(s:|S:)", texto)[1]
    except:
        serie = texto[1:].strip()

    busca = search_series(serie)
    if len(busca[0]) == 0:
        bot.sendMessage(msg['chat']['id'], "Série não encontrado!")
    #else:
    #    num = dividir(busca[0])
    
    # Envie os nomes das séries
    bot.sendMessage(msg['chat']['id'], busca[0])
    #bot.sendMessage(msg['chat']['id'], busca[0][num:])
    ids_series.update({
        msg['chat']['id']: {"complemento": busca[1],
        "legenda": None,
        "epi": None}})
 

def series_ID(msg):
    global ids, ids_series, bot

    # Verificando se é uma série
    if msg['chat']['id'] in ids_series:
        # Checando se alguma linguagem foi escolhida
        if not ids_series[msg['chat']['id']]['epi'] and ids_series[msg['chat']['id']]['complemento']:
            try:
                numero = int(msg['text'])
            except:
                bot.sendMessage(msg['chat']['id'], 'Digite um número válido')

            bot.sendMessage(msg['chat']['id'], "\nEm caso de erro, tente novamente!")
            complemento = ids_series[msg['chat']['id']]['complemento'][numero - 1]
            final_complemento = get_episodes(complemento)

            # Enviando lista para chave "epi" em dict
            ids_series[msg['chat']['id']]['epi'] = final_complemento

            # Caso só tenha legendado, legendado passa a ter índice 0
            if len(final_complemento[1]) != 0 and len(final_complemento[0]) == 0:
                final_complemento[0] = final_complemento[1]

            # Se tiver legendado e dublado, o bot solicita a escolha de um
            if len(final_complemento[1]) != 0:
                bot.sendMessage(msg['chat']['id'], "SELECIONE UM NÚMERO: \n[1] Dublado \n[2] Legendado")
            else:
                # senao, envia 0 para a chave "legenda" no dict
                mensagem = ""
                ids_series[msg['chat']['id']]['legenda'] = 0
                for x in range(1, len(final_complemento[0]) + 1):
                    mensagem += f"[{x}] - EPISÓDIOS\n"
                
                bot.sendMessage(msg['chat']['id'], f"{mensagem}")


        elif ids_series[msg['chat']['id']]['epi']:
            # Neste caso a pessoa já enviou o número do epi
            if ids_series[msg['chat']['id']]['legenda'] == 0 or ids_series[msg['chat']['id']]['legenda'] == 1:           #           Numero da legenda           #
                serie_comple = ids_series[msg['chat']['id']]['epi'][ids_series[msg['chat']['id']]['legenda']][int(msg['text']) - 1]
                url_final = get_filename(serie_comple)

                # url_final2 = get_stream_serie(filename)
                #url_final = "https://www.radiantmediaplayer.com/test-your-streaming-url.html?streamProtocol=mp4&streamUrl=%20" + url_final2.replace("https://", r"https%3A%2F%2F").replace("/", r"%2F").replace("?", r"%3F").replace("=", r"%3D")
                bot.sendMessage(msg['chat']['id'], url_final)
                #start_stream(url_final)
                #Player(url_final)
            else:
                ids_series[msg['chat']['id']]['legenda'] = int(msg['text']) - 1
                mensagem2 = ""
                n = len(ids_series[msg['chat']['id']]['epi'][0])
                for c in range(1, n + 1):
                    mensagem2 += f"[{c}] - EPISÓDIOS\n"

                num = dividir(mensagem2)
                bot.sendMessage(msg['chat']['id'], mensagem2[:num])
                bot.sendMessage(msg['chat']['id'], mensagem2[num:])
        else:
            print("************************************************************\nDesgraça de erro")


def filtro(msg):
    global ids, ids_series, bot

    block = [885905725]
    if msg['chat']['id'] in block:
        pass
    
    texto = None
    if "text" in msg:
        texto = msg['text']

    print("\n" + 35 * "-")
    print(color.cg("Mensagem:"), texto)
    print(color.cg("First Name:"), msg["chat"]["first_name"])
    print(color.cg("Id:"), msg["chat"]["id"])
        
    if texto == "/start" :
        bot.sendMessage(msg['chat']['id'], "Exemplo de uso: f vingadores\nContato: @amaimon02")

    # Se for um filme:
    elif "f" in texto[0] or "F" in texto[0]:
        msg = msg
        filmes(texto, msg)

    # Se for uma série
    elif "s" in texto[0] or "S" in texto[0]:
        msg = msg
        series(texto, msg)

    else:
        filmes_ID(msg)
        series_ID(msg)

bot = telepot.Bot(input('Token: '))
bot.getUpdates()
bot.message_loop(filtro)
input()
