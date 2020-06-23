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
            
    for id_months in months:
        
        file_r = '%s/%s/%s/%s%s.txt' % (destination_path, profile_id, path_file1, path_file2, id_months)
     
        with open(file_r, 'r') as file:			

            text = file.read()
            word_cloud = WordCloud(background_color='white', max_font_size=40).generate(text)
            # plt.figure()
            plt.imshow(word_cloud, interpolation='bilinear')
            plt.title('Nuvem de palavra do mês %s' % (id_months))
            plt.axis('off')
            plt.show()
            

#--------------------------------------------------------------------------------------
def main():

    profiles = ['bolsonaro', 'haddad']	
    generating_word_cloud(profiles[0])

if __name__ == '__main__':
    main()