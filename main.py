from __future__ import absolute_import, print_function

import asyncio
import configparser
import json
import random
import sqlite3
import sys

import matplotlib.pyplot as plt
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

with sqlite3.connect('tweets.db') as conn:
    cur = conn.cursor()
    cur.execute(
        'create table if not exists tweets (created_at text, track text, content text)'
    )
    cur.execute("PRAGMA read_uncommitted = true;")
    conn.commit()


class AssinanteTwitter(StreamListener):
    def __init__(self, name):
        super().__init__(self)
        self.name = name

    def on_data(self, data):
        conteudoJSON = json.loads(data)
        with sqlite3.connect('tweets.db') as conn:
            cur = conn.cursor()
            cur.execute(
                'insert into tweets (created_at, track, content) values (?, ?, ?)',
                (conteudoJSON['created_at'],
                 self.name[0],
                 conteudoJSON['text'])
            )
            conn.commit()
        return True

    def on_error(self, status):
        print(self.name, status)


def get_tweets_by_track() -> list:
    '''
    Realiza uma consulta no banco de dados local retornando uma lista com a quantidade tweets por cada termo pesquisado
    '''
    with sqlite3.connect('tweets.db') as conn:
        cur = conn.cursor()
        cur.execute('select count(*), track from tweets group by track')
        return cur.fetchall()


def show_tweet_graph():
    '''
    Exibe gráfico com base nos registros obtidos da base local
    '''
    labels = []
    sizes = []
    for size, label in get_tweets_by_track():
        labels.append(label)
        sizes.append(size)

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%')
    ax.axis('equal')
    plt.show()


async def stream(track: list):
    '''
    Conecta a API do Twitter e retorna os tweets que estão sendo postados na plataforma em tempo real.
    Essa função é executada durante 10 minutos e depois desconecta o stream.
    Para executá-la é necessário que o arquivo config.ini esteja preenchido com os dados de acesso à API do Twitter.
    '''
    print(f"Iniciando stream para track:{track}")
    await asyncio.sleep(random.randint(10, 20))
    config = configparser.ConfigParser()
    config.read('config.ini')
    if not 'auth' in config.sections():
        raise configparser.NoSectionError("Arquivo de configuração inválido")

    consumer_key = config['auth']['consumer_key']
    consumer_secret = config['auth']['consumer_secret']
    access_token = config['auth']['access_token']
    access_token_secret = config['auth']['access_token_secret']
    assinante = AssinanteTwitter(track)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth=auth, listener=assinante, tweet_mode='extended')
    stream.filter(track=track, is_async=True, languages=["pt"])
    await asyncio.sleep(600)  # Executará durante 10 minutos
    stream.disconnect()


async def main():
    '''
    Função principal que executa simultaneamente as tarefas para obtenção dos dados do Twitter.
    '''
    await asyncio.gather(
        stream(['nfl']),
        stream(['governo']),
        stream(['covid']),
        stream(['dólar']),
        stream(['apple']),
        stream(['economia']),
    )

if 'graph' in sys.argv:
    show_tweet_graph()
else:
    asyncio.run(main())
