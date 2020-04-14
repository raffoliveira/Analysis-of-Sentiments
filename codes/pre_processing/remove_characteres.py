import json, re, gzip
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize.treebank import TreebankWordDetokenizer

# ------------------------------------------------------------------------------

def remove_URL(text):

	return re.sub(r'http\S+', '', text)

# ------------------------------------------------------------------------------

def remove_numbers(text):

	return re.sub(r'\d+','',text)

# ------------------------------------------------------------------------------

def remove_hashtag_mentions(text):

	text = re.sub(r'#\S+', '', text) 
	text = re.sub(r'@\S+', '', text)

	return text

# ------------------------------------------------------------------------------

def remove_punctuation_symbols(text):

	return re.sub(r'[^\w\s]', '', text)

# ------------------------------------------------------------------------------

def remove_stop_words(text):
		 
	stop_words = set(stopwords.words('portuguese')) 
	word_tokens = word_tokenize(text) 
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 

	return TreebankWordDetokenizer().detokenize(filtered_sentence)

# ------------------------------------------------------------------------------

def remove_repeated_letters(text):

	text_tokens = word_tokenize(text)
	new_word = 'text'
	removed_text = []

	for each_word in text_tokens:
		if len(each_word) > 1 and (each_word[-1] == each_word[-2]):			
			for i in range(1, len(each_word)):
				if each_word[-i] == each_word[-(i+1)]:
					new_word = each_word[:-i]
				else:
					break				
			removed_text.append(new_word)
		else:
			removed_text.append(each_word)

	return TreebankWordDetokenizer().detokenize(removed_text)

# ------------------------------------------------------------------------------

def pre_processing(text):

	text = text.lower()
	text = remove_hashtag_mentions(text)
	text = remove_URL(text)
	text = remove_numbers(text)
	text = remove_punctuation_symbols(text)
	text = remove_stop_words(text)		
	text = remove_repeated_letters(text)

	return text

# ------------------------------------------------------------------------------

def writeInFile(file, content):

	file.write('%s\n' % json.dumps(content))

# ------------------------------------------------------------------------------

def processing(profile_id):

	destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
	months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
	file_part1 = 'comments/comments_total.json'
	file_part2 = 'comments/comments_total_processed.json'
	
	for id_months in months:
		file_read = open('%s/%s/%s/%s' % (destination_path, profile_id, id_months, file_part1),'rt')
		file_write = open('%s/%s/%s/%s' % (destination_path, profile_id, id_months, file_part2),'wt')

		for line in file_read:

			comments_processed = []
			id_post = json.loads(line)['id_post']
			comments_total = json.loads(line)['comments']

			for each_comment in comments_total:

				processed_text = pre_processing(each_comment['message'])

				content_comment = {'created_time': each_comment['created_time'],\
						   'id': each_comment['id'],\
						   'message': processed_text,\
						   'comment_count': each_comment['comment_count']}

				comments_processed.append(content_comment)

			content_final = {'id_post': id_post, 'comments': comments_processed}
			writeInFile(file_write, content_final)

		file_read.close()
		file_write.close()

# ------------------------------------------------------------------------------

def main():
	
	profiles = ['bolsonaro', 'haddad']	

	# for id_profile in profiles:

	processing(profiles[1])



if __name__ == '__main__':
	main()