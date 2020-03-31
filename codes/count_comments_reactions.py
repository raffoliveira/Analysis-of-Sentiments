import time, gzip, json, requests, facebook, logging, sys
from time import sleep, strftime
from datetime import datetime
from facebookads.exceptions import FacebookError
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#----------------------------------------------------------------------
def count_posts_total(month, profile):

    total_post = 0

    for id_month in month:
        open_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas/' + profile + '/' + id_month + '/posts/posts_total.json'
        total_post += open(open_path).read().count('\n')
           
    return total_post 

#----------------------------------------------------------------------
def count_reactions(month, profile):

    reactions_total = {'reactions_like': 0, 'reactions_haha': 0, 'reactions_wow': 0, 'reactions_sad': 0, 'reactions_angry': 0, 'reactions_love': 0}
    reactions = ['like', 'haha', 'wow', 'sad', 'angry', 'love']

    for id_month in month:
        file = open('/home/rafael/TCC_II/coleta_TCC_II/coletas/' + profile + '/' + id_month + '/posts/posts_total.json', 'r')

        for line in file:
            for id_reactions in reactions:            
                reactions_total.update({'reactions_'  + id_reactions: reactions_total['reactions_' + id_reactions] + json.loads(line)['reactions_' + id_reactions]['summary']['total_count']})

        file.close()

    return reactions_total

#----------------------------------------------------------------------
def main():

    months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    profiles = ['haddad', 'bolsonaro']

    #total de posts
    number_posts_haddad = count_posts_total(months, profiles[0])
    number_posts_bolsonaro = count_posts_total(months, profiles[1])

    #total de reactions
    count_reactions_haddad = count_reactions(months, profiles[0])
    count_reactions_bolsonaro = count_reactions(months, profiles[1])

    #media: reactions_total/number_posts

    media_reactions_haddad = {}
    media_reactions_bolsonaro = {}

    for key, value in count_reactions_haddad.items():
        media_reactions_haddad.update({key: int(value/number_posts_haddad)})
    print(media_reactions_haddad)
    
    for key, value in count_reactions_bolsonaro.items():
        media_reactions_haddad.update({key: int(value/number_posts_bolsonaro)})   
    print(media_reactions_bolsonaro)
    
    print('\n')
    print(number_posts_haddad)
    print(number_posts_bolsonaro)
    print(count_reactions_haddad)
    print(count_reactions_bolsonaro)    

if __name__ == "__main__":
    main()

