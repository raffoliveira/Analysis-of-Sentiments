import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#--------------------------------------------------------------------------------------
def generating_stem(file_name):

    df = pd.read_csv(file_name, sep = '\t')
    x = df['Created_time']
    y = df['Sentiment_binary']
    plt.stem(x, y, use_line_collection = True)
    plt.title('Evoluição da análise de sentimentos sem pré-processamento Jair Bolsonaro')
    plt.xlabel('Timeline')
    plt.ylabel('Scores')
    plt.savefig('Bolsonaro.png', dpi = 300)
    plt.show()

#--------------------------------------------------------------------------------------
def main():    

    profiles = ['bolsonaro', 'haddad']
    file_csv = '/home/rafael/TCC_II/coleta_TCC_II/codes/converting_files/%s/Sentiments/comments_total_sentiment.csv' % (profiles[0])
    generating_stem(file_csv)

if __name__ == '__main__':
    main()