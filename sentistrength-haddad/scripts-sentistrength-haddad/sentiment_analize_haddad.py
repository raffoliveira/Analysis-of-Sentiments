import json
from sentistrength import PySentiStr


def store(estrutura_de_dados, arq):
    with open(arq, 'w', encoding='utf8') as arquivo:
        json.dump(estrutura_de_dados, arquivo, sort_keys=True, indent=4, ensure_ascii=False)




senti = PySentiStr()
senti.setSentiStrengthPath(r'/home/lucas/Documentos/sentistrength/SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath(r'/home/lucas/Documentos/sentistrength/SentiStrength_Data/')


# lemos o JSON em disco
data = open('2019-12-12-tweets-fernando-haddad-com-texto-completo.txt').read()

tweets_haddad = json.loads(data)

tweets_with_sentiment_analize = []
for tweet in tweets_haddad:
    try:
        if tweet['pre_processed_full_text'].__len__() == 0:
            print(tweet['index'])
            tweet['score_binary'] = [(1, -1)]
            tweet['score_scale'] = [0.0]
            continue

        text_get_sentiment = ' '
        text_get_sentiment = text_get_sentiment.join(tweet['pre_processed_full_text'])
        result_binary = senti.getSentiment(text_get_sentiment, score='binary')
        result_scale = senti.getSentiment(text_get_sentiment, score='scale')
        print('text_get_sentiment: '+ text_get_sentiment)
        print(result_binary)
        print(result_scale)

        tweet['score_binary'] = result_binary
        tweet['score_scale'] = result_scale

        tweets_with_sentiment_analize.append(tweet)

    except Exception as msg:
        print('analisado até: '+str(tweet['index']))
        break

store(tweets_with_sentiment_analize,'2019-12-12-tweets-fernando-haddad-com-analise-sentimentos.txt')
