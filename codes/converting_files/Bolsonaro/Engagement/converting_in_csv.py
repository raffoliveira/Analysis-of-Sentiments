import csv, json
from datetime import datetime

#--------------------------------------------------------------------------------------
def convertDateInUnixTimeStamp(stime):
	return '%s' % (datetime.strptime(stime, "%Y-%m-%dT%H:%M:%S+0000").timestamp())

#--------------------------------------------------------------------------------------
def converting_files(profile_id):

	destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
	months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
	path_file = 'posts/posts_total.json'
	file_w = 'bolsonaro_likes.tsv'
	data_like = [['Counter', 'Created_time', 'Time_Stamp', 'ID', 'Message', 'Shares', 'Status_type', 
	'Full_Picture', 'Reactions_like', 'Reactions_haha', 'Reactions_wow', 'Reactions_sad', 'Reactions_angry',
	'Reactions_love']]
	count_day = 0

	for id_months in months:

		file_r = '%s/%s/%s/%s' % (destination_path, profile_id, id_months, path_file)

		with open(file_r, 'r') as file_read:			

			for line in file_read:

				created_time = json.loads(line)['created_time']
				time_stamp = convertDateInUnixTimeStamp(created_time)
				id_post = json.loads(line)['id']
				message = json.loads(line)['message']
				shares = json.loads(line)['shares']['count']
				status_type = json.loads(line)['status_type']
				full_picture = json.loads(line)['full_picture']
				like_post = json.loads(line)['reactions_like']['summary']['total_count']
				haha_post = json.loads(line)['reactions_haha']['summary']['total_count']
				wow_post = json.loads(line)['reactions_wow']['summary']['total_count']
				sad_post = json.loads(line)['reactions_sad']['summary']['total_count']
				angry_post = json.loads(line)['reactions_angry']['summary']['total_count']
				love_post = json.loads(line)['reactions_love']['summary']['total_count']

				data_like.append([count_day, created_time, time_stamp, id_post, message, shares, status_type,
				full_picture, like_post, haha_post, wow_post, sad_post, angry_post, love_post])

				count_day += 1			

	with open(file_w, 'w') as file_write:
		writer = csv.writer(file_write, delimiter = '\t')
		writer.writerows(data_like)

#--------------------------------------------------------------------------------------
def main():

	profiles = ['bolsonaro', 'haddad']	
	converting_files(profiles[0])

if __name__ == '__main__':
	main()