import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
sns.set(style="darkgrid")

#--------------------------------------------------------------------------------------
def generating_scatterplot(file_name):

        df = pd.read_csv(file_name, sep = '\t')
        cmap = sns.cubehelix_palette(dark = .3, light = .8, as_cmap = True)
        sns.relplot(x = 'Created_time', y = 'Reactions_angry', hue = 'Reactions_angry', size = 'Reactions_angry', palette = cmap, data = df)
        plt.title('Engajamento de reações bravas de Jair Bolsonaro')
        # plt.xlabel('Timeline')
        plt.ylabel('Números de reações bravas')
        months =  ['Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        plt.xticks([0, 73, 111, 190, 192], months, rotation = 90)
        plt.show()

#--------------------------------------------------------------------------------------
def main():

        profiles = ['Bolsonaro', 'Haddad']
        file_final_tsv = '/home/rafael/TCC_II/coleta_TCC_II/codes/converting_files/%s/Engagement/bolsonaro_posts.tsv'	% (profiles[0])
        generating_scatterplot(file_final_tsv)

if __name__ == '__main__':
        main()