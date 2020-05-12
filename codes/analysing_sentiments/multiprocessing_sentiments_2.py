import json, time
from sentistrength import PySentiStr
import multiprocess as mp

senti = PySentiStr()
senti.setSentiStrengthPath('/home/rafael_oliveira/coleta_TCC_II/codes/sentistrength/SentiStrength.jar')
senti.setSentiStrengthLanguageFolderPath('/home/rafael_oliveira/coleta_TCC_II/codes/sentistrength/SentiStrength_Data/')

# ------------------------------------------------------------------------------

def writeInFile(file, content):

	file.write('%s\n' % json.dumps(content))

# ------------------------------------------------------------------------------

def processing_Sentiment(message):

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

def analysing_Sentiments(id_month, id_file_part, profile_id):

	destination_path = '/home/rafael_oliveira/coleta_TCC_II/coletas'

	file_read = open('%s/%s/%s/comments/%s.json' % (destination_path, profile_id, id_month, id_file_part),'rt')
	file_write = open('%s/%s/%s/comments/%s_sentiment.json' % (destination_path, profile_id, id_month, id_file_part),'wt')

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

def dividing_Into_Processes(profile_id):

	month = 'outubro'
	file_part = ['comments_total_processed_with_stop_words', 'comments_total_processed_without_stop_words']
	processes = []

	for id_file_part in file_part:
		proc = mp.Process(target=analysing_Sentiments, args=(month, id_file_part, profile_id))
		processes.append(proc)
		proc.start()

	for proc in processes:
		proc.join()	

# ------------------------------------------------------------------------------

def main():

	profiles = ['bolsonaro', 'haddad']

	log_file = open('log.txt', 'w')	

	# for id_profile in profiles:

	starttime = time.time()		
	dividing_Into_Processes(profiles[0])
	log_file.write('\nThe processing of {} took {} seconds.'.format(profiles[0], time.time()-starttime))

if __name__ == '__main__':
	main()
