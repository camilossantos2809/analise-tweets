from __future__ import absolute_import, print_function

import asyncio
import configparser
import json

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener


class AssinanteTwitter(StreamListener):

    def on_data(self, data):
        conteudoJSON = json.loads(data)
        print(conteudoJSON["text"])
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
    assinante = AssinanteTwitter()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, assinante)
    stream.filter(track=track, is_async=True, languages=["pt"])


async def main():
    await asyncio.gather(
        stream(['marvel']),
        stream(['presidente'])
    )

asyncio.run(main())
