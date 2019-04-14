from __future__ import absolute_import, print_function

import asyncio
import configparser
import json
import sqlite3

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener


with sqlite3.connect('tweets.db') as conn:
    cur = conn.cursor()
    cur.execute(
        'create table if not exists tweets (created_at text, track text, content text)')
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
        print(status)


async def stream(track: list):
    print(f"Iniciando stream para track:{track}")
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
    stream = Stream(auth, assinante)
    stream.filter(track=track, is_async=True, languages=["pt"])
    await asyncio.sleep(10)
    stream.disconnect()


async def main():
    await asyncio.gather(
        stream(['marvel']),
        stream(['presidente']),
        stream(['música']),
        stream(['futebol']),
        stream(['religião']),
        stream(['tecnologia'])
    )

asyncio.run(main())
