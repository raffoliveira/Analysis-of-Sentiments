import json

# lemos o JSON em disco
data = open('2019-12-12-tweets-fernando-haddad-com-analise-sentimentos.txt').read()

tweets_haddad = json.loads(data)

count_negative = 0.0
count_positive = 0.0
count_neutre = 0.0

for tweet in tweets_haddad:
    if tweet['score_scale'][0] < 0.0:
        count_negative +=1
    elif tweet['score_scale'][0] > 0.0:
        count_positive +=1
    else:
        count_neutre+=1

print('negative tweets: {0}'.format(str((count_negative/tweets_haddad.__len__())*100)))
print('positive tweets: {0}'.format(str((count_positive/tweets_haddad.__len__())*100)))
print('neutre tweets: {0}'.format(str((count_neutre/tweets_haddad.__len__())*100)))