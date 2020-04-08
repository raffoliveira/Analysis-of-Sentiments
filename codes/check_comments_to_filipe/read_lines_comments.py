import json, gzip

def main():

	destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
	profile = ['bolsonaro', 'haddad']
	months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
	file_part1 = 'posts_comments_%s_' % profile[0]
	file_data = '2018-10-28_2018-10-29'

	file_name = '%s/%s/%s/%s%s.json.gz' % (destination_path, profile[0], months[2], file_part1, file_data)

	with gzip.open(file_name) as file_Main:

		for line in file_Main:
			json_line = json.loads(line.strip())
			id_post = json_line['id_post']

			if id_post == '211857482296579_244838876192161':

				for i in range(10):
					comments_list = json_line['comments']
					print('comment %d: %s' % (i + 1, comments_list[i]['message']))

	file_Main.close()



if __name__ == "__main__":
	main()