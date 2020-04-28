import json

def writeInFile(file, content):

	file.write('%s\n' % json.dumps(content))

# ------------------------------------------------------------------------------

def count_Comments(profile_id):

	destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
	months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
	
	for id_months in months:

		file_read = open('%s/%s/%s/comments/comments_total.json' % (destination_path, profile_id, id_months),'rt')
		file_write = open('%s/%s/%s/comments/counter_comments.json' % (destination_path, profile_id, id_months),'wt')
		counter_comments = {}

		for line in file_read:
			
			id_post = json.loads(line)['id_post']
			comments_total = json.loads(line)['comments']

			#{'id_post': number_comments}
			content = {'id_post': len(comments_total)}
			counter_comments.append(content)
			writeInFile(file_write, content)

		final_line = 'The total of comments in {id_months} is {sum(counter_comments.values())}'
		writeInFile(file_write, final_line)
		file_read.close()
		file_write.close()

# ------------------------------------------------------------------------------

def main():

	profiles = ['bolsonaro', 'haddad']	

	for id_profile in profiles:
		
		count_Comments(id_profile)

if __name__ == '__main__':
	main()