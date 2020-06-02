import csv, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
sns.set(style="darkgrid")

#--------------------------------------------------------------------------------------
def convertDateInUnixTimeStamp(stime):
	return '%s' % (datetime.strptime(stime, "%Y-%m-%dT%H:%M:%S+0000").timestamp())

#--------------------------------------------------------------------------------------
def converting_likes(profile_id):

	destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
	months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
	path_file = 'posts/posts_total.json'
	file_w = 'bolsonaro_likes.tsv'
	data_like = [['Counter', 'Date_Post', 'Time_Stamp', 'Total_likes']]
	count_day = 0

	for id_months in months:

		file_r = '%s/%s/%s/%s' % (destination_path, profile_id, id_months, path_file)

		with open(file_r, 'r') as file_read:			

			for line in file_read:

				date_post = json.loads(line)['created_time']
				time_stamp = convertDateInUnixTimeStamp(date_post)
				likes_post = json.loads(line)['reactions_like']['summary']['total_count']
				data_like.append([count_day, date_post, time_stamp, likes_post])
				count_day += 1
			

	with open(file_w, 'w') as file_write:
		writer = csv.writer(file_write, delimiter = '\t')
		writer.writerows(data_like)

	file_final_tsv = '/home/rafael/TCC_II/coleta_TCC_II/codes/converting_files/bolsonaro_likes.tsv'

	generating_scatterplot(file_final_tsv)

#--------------------------------------------------------------------------------------
def generating_scatterplot(file_name):

	data_likes = pd.read_csv(file_name, sep = '\t')
	cmap = sns.cubehelix_palette(dark = .3, light = .8, as_cmap = True)
	sns.relplot(x = 'Counter', y = 'Total_likes', hue = 'Total_likes', legend = False, size = 'Total_likes',
	palette = cmap, data = data_likes)
	plt.title('Timeline do engajamento de likes de Jair Bolsonaro')
	plt.xlabel('Timeline')
	plt.ylabel('Número de likes')
	plt.savefig('Timeline_likes_Bolsonaro.png', dpi = 300)
	plt.show()


#--------------------------------------------------------------------------------------
def main():

	profiles = ['bolsonaro', 'haddad']	
	converting_likes(profiles[0])

if __name__ == '__main__':
	main()