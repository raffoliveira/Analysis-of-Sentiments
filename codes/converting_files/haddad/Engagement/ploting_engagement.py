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
        sns.relplot(x = 'Created_time', y = 'Shares', hue = 'Shares', size = 'Shares', palette = cmap, data = df)
        plt.title('Engajamento de Compartilhamento (shares) de Fernando Haddad')
        plt.xlabel('Timeline')
        plt.ylabel('Números de compartilhamentos')
        months =  ['Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        plt.xticks([0, 101, 321, 556, 562], months, rotation = 90)
        plt.show()

#--------------------------------------------------------------------------------------
def main():

        profiles = ['bolsonaro', 'haddad']
        file_final_tsv = '/home/rafael/TCC_II/coleta_TCC_II/codes/converting_files/%s/Engagement/%s_posts.tsv'	% (profiles[1], profiles[1])
        generating_scatterplot(file_final_tsv)

if __name__ == '__main__':
        main()