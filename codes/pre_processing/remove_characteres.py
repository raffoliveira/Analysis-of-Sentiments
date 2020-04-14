import json, re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize.treebank import TreebankWordDetokenizer


# ------------------------------------------------------------------------------

def remove_URL(text):

	return re.sub(r'http\S+', '', text) #re.sub(pattern, repl, string)

# ------------------------------------------------------------------------------

def remove_numbers(text):

	return re.sub(r'\d+','',text)

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

def main():

	original_text = 'Falaaaa a porque aeeeee #falar, b4lz? bom #dmaissss esta vaca e @fald na https://fdfjdo.vdo.com fldlfmlsdsaaaaaa ae mannnooooooo'
	print('Original text: %s' % original_text)
	new_text = original_text

	new_text = new_text.lower()
	new_text = remove_hashtag_mentions(new_text)
	new_text = remove_URL(original_text)
	new_text = remove_numbers(new_text)
	new_text = remove_punctuation_symbols(new_text)
	new_text = remove_stop_words(new_text)		
	new_text = remove_repeated_letters(new_text)

	print('\nProcessed text: %s' % new_text)

if __name__ == '__main__':
	main()