import time, gzip, json, requests, facebook, logging, sys
from time import sleep, strftime
from datetime import datetime
from random import shuffle
from matplotlib import gridspec
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
                reactions_total.update({'reactions_'  + id_reactions: reactions_total['reactions_' + id_reactions]\
                                     + json.loads(line)['reactions_' + id_reactions]['summary']['total_count']})

        file.close()

    return reactions_total

#----------------------------------------------------------------------
def main():

    months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    profiles = ['haddad', 'bolsonaro']
    reactions = ['like', 'haha', 'wow', 'sad', 'angry', 'love']
 
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


    #--------------------------Pie chart--------------------------------

    reactions_keys_haddad = list(count_reactions_haddad.keys())
    reactions_values_haddad = list(count_reactions_haddad.values())
    reactions_keys_bolsonaro = list(count_reactions_bolsonaro.keys())
    reactions_values_bolsonaro = list(count_reactions_bolsonaro.values())

    sum_all_reactions_haddad = sum(reactions_values_haddad)
    sum_all_reactions_bolsonaro = sum(reactions_values_bolsonaro)

    # reactions_legend_haddad = []
    # reactions_legend_bolsonaro = []

    # for i, j in zip(reactions, reactions_values_haddad):
    #     reactions_legend_haddad.append(i + ': ' + str(round(((j/sum_all_reactions_haddad)*100),2)) + '%')

    # for i, j in zip(reactions, reactions_values_bolsonaro):
    #     reactions_legend_bolsonaro.append(i + ': ' + str(round(((j/sum_all_reactions_bolsonaro)*100),2)) + '%')

    #---------------------------------hadddad-------------------------------------------

    # print(reactions_values_haddad)
    # print(reactions_values_bolsonaro)
    # print(reactions)
    # print(count_reactions_haddad)
    # print(count_reactions_bolsonaro)

    groups = 6
    barWidth = 0.35

    fig = plt.figure()
    ax = fig.subplots()
    index = np.arange(groups)
    
    # Create horizontal bars
    rects1 = ax.barh(index, reactions_values_haddad, barWidth, color = ('#66B3FF'), label = 'Haddad')
    rects2 = ax.barh(index + barWidth, reactions_values_bolsonaro, barWidth, color = ('#99FF99'), label = 'Bolsonaro')
     
    # Create names on the y-axis
    plt.yticks(index + 0.2, reactions)

    totals = []
    for i in ax.patches:
        totals.append(i.get_width())

    total = sum(totals)

    for i, j in zip(ax.patches, reactions_values_haddad):
        ax.text(i.get_width() + .3, i.get_y() + .20, j, color = 'dimgrey')

    for i, j in zip(ax.patches, reactions_values_bolsonaro):
        ax.text(i.get_width() + 5.50, i.get_y() + .60, j, color = 'dimgrey')

    ax.invert_yaxis()

    plt.tight_layout()
    plt.legend()
    plt.title('Distribuição de reactions')

    # Show graphic
    plt.show()






    

if __name__ == "__main__":
    main()
