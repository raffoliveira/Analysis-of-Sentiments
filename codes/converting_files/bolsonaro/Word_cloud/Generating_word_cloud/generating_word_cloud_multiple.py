import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import json

#--------------------------------------------------------------------------------------
def generating_word_cloud(profile_id):

    destination_path = '/home/rafael/TCC_II/coleta_TCC_II/codes/converting_files'
    months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro', 'todos']
    path_file1 = 'Word_cloud/Generating_texts'
    path_file2 = 'text_word_cloud_'   
   
    fig, ((ax0, ax1, ax2), (ax3, ax4, ax5)) = plt.subplots(2,3)
    fig.suptitle('Nuvens de palavras Jair Bolsonaro')

    for axs, id_months in enumerate(months): 

        file_r = '%s/%s/%s/%s%s.txt' % (destination_path, profile_id, path_file1, path_file2, id_months)
        var = 'ax%s' % (axs)
    
        with open(file_r, 'r') as file:			

            text = file.read()
            word_cloud = WordCloud(background_color='white', max_font_size=40).generate(text)
            vars()[var].imshow(word_cloud, interpolation='bilinear')
            vars()[var].set_title('%s' % (id_months))
            vars()[var].axis('off')

    plt.savefig('multiple.png', dpi=300)    
    plt.show()
                                  

#--------------------------------------------------------------------------------------
def main():

    profiles = ['bolsonaro', 'haddad']	
    generating_word_cloud(profiles[0])

if __name__ == '__main__':
    main()