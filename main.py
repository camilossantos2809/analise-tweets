from __future__ import absolute_import, print_function

import json

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener


class AssinanteTwitter(StreamListener):
    # Essa funÃ§Ã£o serÃ¡ invocada automaticamente toda vez que um twitter for identificado
    def on_data(self, data):
        conteudoJSON = json.loads(data)
        print(conteudoJSON["text"])
        return True

    # Essa funÃ§Ã£o serÃ¡ invocada automaticamente toda vez que ocorrer um erro
    def on_error(self, status):
        print(status)


# Para executar esse exemplo Ã© preciso possuir uma conta no twitter,
# caso nÃ£o possua crie uma.
# Entre no site http://apps.twitter.com e crie uma nova applicaÃ§Ã£o preenchendo as informaÃ§Ãμes
# SerÃ¡ gerado o consumer key e o consumer secret, que sÃ£o a identificaÃ§Ã£o de sua aplicaÃ§Ã£o no twitter.
print("Inicio do programa")
consumer_key = ""
consumer_secret = ""
# VocÃa serÃ¡ redirecionado para outra pÃ¡gina, clique na aba 'Keys and Access Tokens'
# Crie um token de acesso novo, ele serÃ¡ utilizado no lugar de suas credenciais
access_token = ""
access_token_secret = ""
assinante = AssinanteTwitter()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, assinante)
stream.filter(track=['música'], languages=["pt"])
