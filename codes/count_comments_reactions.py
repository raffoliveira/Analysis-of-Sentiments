import time, gzip, json, requests, facebook, logging, sys
from time import sleep, strftime
from datetime import datetime
from random import shuffle
from facebookads.exceptions import FacebookError
from requests.exceptions import HTTPError
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


    #--------------------------bakery/pie plot--------------------------------

    reactions_keys_haddad = list(count_reactions_haddad.keys())
    reactions_values_haddad = list(count_reactions_haddad.values())
    reactions_keys_bolsonaro = list(count_reactions_bolsonaro.keys())
    reactions_values_bolsonaro = list(count_reactions_bolsonaro.values())

    sum_all_reactions_haddad = sum(reactions_values_haddad)
    sum_all_reactions_bolsonaro = sum(reactions_values_bolsonaro)

    reactions_legend_haddad = []
    reactions_legend_bolsonaro = []

    for i, j in zip(reactions, reactions_values_haddad):
        reactions_legend_haddad.append(i + ': ' + str(round(((j/sum_all_reactions_haddad)*100),2)) + '%')

    for i, j in zip(reactions, reactions_values_bolsonaro):
        reactions_legend_bolsonaro.append(i + ': ' + str(round(((j/sum_all_reactions_bolsonaro)*100),2)) + '%')

    #---------------------------------hadddad-------------------------------------------

    fig1 = plt.figure(figsize=(8,5))
    
    gs1 = gridspec.GridSpec(1, 1, left = 0.1, right = 0.7, bottom = 0.1, top = 0.7,)
    gs2 = gridspec.GridSpec(1, 1, left = 0.05, right = 0.95, bottom = 0.9, top = 1.0,)

    pie_ax = fig1.add_subplot(gs1[0])
    title_ax = fig1.add_subplot(gs2[0])

    # Create a list of colors (from iWantHue)
    colors = ['#FF9999','#66B3FF','#99FF99','#FFCC99', '#FDFF83', '#CBC3FA']

    # Create a pie chart
    wedges, texts = pie_ax.pie(reactions_values_haddad, shadow = False, colors = colors, startangle = 90)

    bbox_props = dict(boxstyle = "square, pad = 0.3", fc = "w", ec = "k", lw = 0.72)
    kw = dict(xycoords = 'data', textcoords = 'data', arrowprops = dict(arrowstyle = "-"), zorder = 0, va = "center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle, angleA = 0, angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle, "color": colors[i]})
        pie_ax.annotate(reactions_legend_haddad[i], xy = (x, y), xytext = (1.35*np.sign(x), 1.4*y),\
            horizontalalignment = horizontalalignment, **kw)

    # View the plot drop above
    pie_ax.axis('equal')

    title_ax.set_facecolor('w')

    title_ax.text(0.5, 0.5, "Distribuição de Reactions Haddad", ha = "center", va = "center",\
        transform = title_ax.transAxes, color = "k")

    for side in ['top', 'bottom', 'left', 'right']:
        title_ax.spines[side].set_visible(False)

    title_ax.axes.get_xaxis().set_visible(False)    
    title_ax.axes.get_yaxis().set_visible(False)
    plt.savefig(r"reactions_total_haddad.png",bbox_inches="tight")

    #--------------------------------bolsonaro-------------------------------------

    fig2 = plt.figure(figsize=(8,5))
    
    gs3 = gridspec.GridSpec(1, 1, left = 0.1, right = 0.7, bottom = 0.1, top = 0.7,)
    gs4 = gridspec.GridSpec(1, 1, left = 0.05, right = 0.95, bottom = 0.9, top = 1.0,)

    pie_ax1 = fig2.add_subplot(gs3[0])
    title_ax1 = fig2.add_subplot(gs4[0])

    # Create a pie chart
    wedges1, texts1 = pie_ax1.pie(reactions_values_bolsonaro, shadow = False, colors = colors, startangle = 90)

    bbox_props1 = dict(boxstyle = "square, pad = 0.3", fc = "w", ec = "k", lw = 0.72)
    kw1 = dict(xycoords = 'data', textcoords = 'data', arrowprops = dict(arrowstyle = "-"), zorder = 0, va = "center")

    for i, p in enumerate(wedges1):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle, angleA = 0, angleB={}".format(ang)
        kw1["arrowprops"].update({"connectionstyle": connectionstyle, "color": colors[i]})
        pie_ax1.annotate(reactions_legend_bolsonaro[i], xy = (x, y), xytext = (1.35*np.sign(x), 1.4*y),\
            horizontalalignment = horizontalalignment, **kw1)

    # View the plot drop above
    pie_ax1.axis('equal')

    title_ax1.set_facecolor('w')

    title_ax1.text(0.5, 0.5, "Distribuição de Reactions Bolsonaro", ha = "center", va = "center",\
        transform = title_ax1.transAxes, color = "k")

    for side in ['top', 'bottom', 'left', 'right']:
        title_ax1.spines[side].set_visible(False)

    title_ax1.axes.get_xaxis().set_visible(False)    
    title_ax1.axes.get_yaxis().set_visible(False)  

    plt.savefig(r"reactions_total_bolsonaro.png",bbox_inches="tight")
    plt.show()














    # fig, (ax1, ax2) = plt.subplots(1,2)

    # wedges1, texts1, autotexts1 = ax1.pie(reactions_values_haddad, colors = colors, autopct = '%1.1f%%', \
    #                                 startangle = 90, pctdistance = 1.1)
    # wedges2, texts2, autotexts2 = ax2.pie(reactions_values_bolsonaro, colors = colors, autopct = '%1.1f%%', \
    #                                 startangle = 90, pctdistance = 1.1)

    # #draw center circle
    # # centre_circle = plt.Circle((0,0), 0.90, fc = 'white')
    # # fig = plt.gcf()
    # # fig.gca().add_artist(centre_circle)

    # # change labels color
    # for text1, text2 in zip(texts1, texts2):
    #     text1.set_color('grey')
    #     text2.set_color('grey')

    # for autotext1, autotext2 in zip(autotexts1, autotexts2):
    #      autotext1.set_color('grey')
    #      autotext2.set_color('grey')

    # ax1.axis('equal')  #equal aspect ratio ensures that pie is drawn as a circle
    # ax2.axis('equal')  #equal aspect ratio ensures that pie is drawn as a circle

    # ax1.legend(wedges1, reactions_keys_haddad, loc = 'best', bbox_to_anchor = (1, 0, 0, 1))
    # # ax2.legend(wedges, reactions_keys_bolsonaro, loc = 'center left', bbox_to_anchor = (1, 0, 0.5, 1))

    # ax1.set_title('Distribuição Reactions Haddad')
    # ax2.set_title('Distribuição Reactions Bolsonaro')


    # plt.tight_layout()
    # # plt.savefig('reactions_total.png', dpi = 300)
    # plt.show()

if __name__ == "__main__":
    main()
