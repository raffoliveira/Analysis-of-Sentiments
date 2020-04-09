import json, re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# nltk = natural language tool kit
# re = regular expression operations 

def remove_URL(text):

	return re.sub(r'http\S+', '', text) #re.sub(pattern, repl, string)


def remove_simbols(text):

	return re.sub(r'[^\w\s]','',text)


def remove_numbers(text):

	return re.sub(r'\d+','',text)


def remove_repeated_letters(text):

	text_tokens = word_tokenize(text)

	text_processed = [''.join(sorted(set(i), key = i.index)) for i in text_tokens]

	return text_processed


def remove_punctuation(text):

	new_words = []
	for word in text:
		new_word = re.sub(r'[^\w\s]', '', word)
		if new_word != '':
			new_words.append(new_word)
	return new_words


def replace_stop_words(text):
		 
	stop_words = set(stopwords.words('portuguese')) 	  
	word_tokens = word_tokenize(text) 
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 

	return filtered_sentence


def main():

	original_text = 'É agradecer? a 4Deus a 2cada talvez a manhã pelo milagre da vida!! #deulivre Meu Email é raf@gmail.com e meu site\
	segue https://rafadf.fd.com.br'
	print('original text: %s' % original_text)

	new_text = remove_URL(original_text)
	new_text = new_text.lower()
	# new_text = remove_repeated_letters(new_text)
	new_text = remove_numbers(new_text)
	new_text = replace_stop_words(new_text)
	new_text = remove_punctuation(new_text)
	print('\nprocessed text: %s' % new_text)

if __name__ == '__main__':
	main()