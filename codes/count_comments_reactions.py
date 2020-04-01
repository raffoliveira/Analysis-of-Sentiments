import time, gzip, json, requests, facebook, logging, sys
from time import sleep, strftime
from datetime import datetime
from random import shuffle
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
def func(pct, allvals):

    absolute = int(pct/100.*np.sum(allvals))

    return '{:.1lf} % \n ({:d})'.format(pct, absolute)

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

    for key, value in count_reactions_bolsonaro.items():
        media_reactions_bolsonaro.update({key: int(value/number_posts_bolsonaro)})


    #--------------------------bakery/pie plot--------------------------------

    reactions_key = count_reactions_haddad.keys()
    reactions_value = count_reactions_haddad.values()
    reactions_info = []

    # #Pie chart
    for key, value in count_reactions_haddad.items():
        reactions_info.append(key + ': ' + str(value))

    #explode the 4th slice
    # explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05)

    #add colors
    colors = ['#FF9999','#66B3FF','#99FF99','#FFCC99', '#FDFF83', '#CBC3FA']

    fig, ax = plt.subplots()

    wedges, texts, autotexts = ax.pie(reactions_value, colors = colors, autopct = '%1.1f%%', startangle = 90, pctdistance = 0.85)

    #draw center circle
    centre_circle = plt.Circle((0,0), 0.70, fc = 'white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # change labels color
    for text in texts:
         text.set_color('grey')

    for autotext in autotexts:
         autotext.set_color('grey')

    ax.axis('equal')  #equal aspect ratio ensures that pie is drawn as a circle

    ax.legend(wedges, reactions_info, loc = 'center left', bbox_to_anchor = (1, 0, 0.5, 1))

    ax.set_title('Distribuição total de reactions')
    plt.tight_layout()
    plt.savefig('reactions_total.png', dpi = 300)
    plt.show()

if __name__ == "__main__":
    main()
