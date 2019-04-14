# Análise de tweets (stream)

Aplicativo de exemplo para consumo de API do Twitter utilizando o [tweepy](https://tweepy.readthedocs.io/en/v3.5.0/index.html). A aplicação insere em um banco de dados local os tweets que estão sendo postados em tempo real pelos usuários da plataforma de acordo as palavras chave informadas. Posteriomente é possível emitir um gráfico que exibe a quantidade de tweets para cada palavra chave.

# Instalação

Instale o [pipenv](https://github.com/pypa/pipenv) para gerenciar o ambiente virtual e as dependências.

    pip install pipenv

Acesse o diretório do projeto.

    cd /<diretorio_do_projeto>/analise_tweets

Crie um ambiente virtual com o python 3.7.

    pipenv --python 3.7

O projeto já possui o arquivo **Pipfile** configurado, basta executar o comando do pipenv para instalação das dependências.

    pipenv install

Preencha o arquivo de configuração `config.ini` com os dados de acesso disponibilizados pelo Twitter.

    [auth]
    consumer_key=123456789
    consumer_secret=123456789
    access_token=123456789
    access_token_secret=123456789

Com isso o código já poderá ser executado.

    pipenv run python main.py

Após os 10 minutos coletando os dados os tweets estarão armazenados no arquivo do SQLite **tweets.db**.

Execute o comando abaixo para visualizar os dados coletados no gráfico.

    pipenv run python main.py graph
