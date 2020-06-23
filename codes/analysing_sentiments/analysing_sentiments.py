import json
from sentistrength import PySentiStr

senti = PySentiStr()
senti.setSentiStrengthPath('/home/rafael/TCC_II/coleta_TCC_II/codes/sentistrength/SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('/home/rafael/TCC_II/coleta_TCC_II/codes/sentistrength/SentiStrength_Data/')

# ------------------------------------------------------------------------------

def writeInFile(file, content):

	file.write('%s\n' % json.dumps(content))

# ------------------------------------------------------------------------------

def processing_Sentiment(message):

	print(f'THE MESSAGE IS: {message}')

	scores = ['dual', 'binary', 'trinary', 'scale']
	text_sentiments = {}

	if message != '':

		for id_scores in scores:

			result_sentiment = senti.getSentiment(message, score = id_scores)
			text_sentiments.update({id_scores: result_sentiment})

		return text_sentiments
	else:

		return text_sentiments

# ------------------------------------------------------------------------------

def analysing_Sentiments(profile_id):

	destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
	months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
	file_part = ['comments_total', 'comments_total_processed_with_stop_words', \
				'comments_total_processed_without_stop_words']

	for id_months in months:

		for id_file_part in file_part:

			file_read = open('%s/%s/%s/comments/%s.json' % (destination_path, profile_id, id_months, id_file_part),'rt')
			file_write = open('%s/%s/%s/comments/%s_sentiment.json' % (destination_path, profile_id, id_months, id_file_part),'wt')

			for line in file_read:

				comments_processed = []
				id_post = json.loads(line)['id_post']
				comments_total = json.loads(line)['comments']

				for each_comment in comments_total:

					processed_text = processing_Sentiment(each_comment['message'])

					content_comment = {'created_time': each_comment['created_time'],\
						   'id': each_comment['id'],\
						   'message': each_comment['message'],\
						   'comment_count': each_comment['comment_count'],\
						   'sentiment_scores': processed_text}

					comments_processed.append(content_comment)

				content_final = {'id_post': id_post, 'comments': comments_processed}
				writeInFile(file_write, content_final)

			file_read.close()
			file_write.close()

# ------------------------------------------------------------------------------

def main():

	profiles = ['bolsonaro', 'haddad']	

	for id_profile in profiles:
		
		analysing_Sentiments(id_profile)

if __name__ == '__main__':
	main()