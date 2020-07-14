import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#--------------------------------------------------------------------------------------
def generating_stem(file_name):

    df = pd.read_csv(file_name, sep = '\t')
    date_df_dezembro = df[df['Month'] > 11]
    print(date_df_dezembro.head())
    x = date_df_dezembro['Created_time']
    y = date_df_dezembro['Sentiment_binary']
    plt.stem(x, y, linefmt = 'grey', use_line_collection = True)
    plt.title('Evoluição da análise de sentimentos sem pré-processamento Jair Bolsonaro no mês de Novembro/18')
    plt.xlabel('Timeline')
    plt.ylabel('Scores')
    plt.figure(figsize = (20,10))
    plt.savefig('Bolsonaro.png', dpi = 300)
    # plt.show()

#--------------------------------------------------------------------------------------
def main():    

    profiles = ['bolsonaro', 'haddad']
    file_csv = '/home/rafael/TCC_II/coleta_TCC_II/codes/converting_files/%s/Sentiments/' \
        'Converting_files/comments_total_sentiment.csv' % (profiles[0])
    generating_stem(file_csv)

if __name__ == '__main__':
    main()