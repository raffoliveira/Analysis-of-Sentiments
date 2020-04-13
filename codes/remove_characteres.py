# https://www.nltk.org/index.html
import json, re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize.treebank import TreebankWordDetokenizer

# nltk = natural language tool kit
# re = regular expression operations 

# ------------------------------------------------------------------------------

def remove_URL(text):

	return re.sub(r'http\S+', '', text) #re.sub(pattern, repl, string)

# ------------------------------------------------------------------------------

def remove_simbols(text):

	return re.sub(r'[^\w\s]','',text)

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

def remove_hashtag(text):

	word_tokens = word_tokenize(text)

	print(word_tokens)

	for id_word in word_tokens:
		if id_word[0] == '#':
			word_tokens.remove(id_word)

	return TreebankWordDetokenizer().detokenize(word_tokens)

# ------------------------------------------------------------------------------

def remove_punctuation(text):

	new_words = []
	for word in text:
		new_word = re.sub(r'[^\w\s]', '', word)
		if new_word != '':
			new_words.append(new_word)
	return new_words

# ------------------------------------------------------------------------------

def replace_stop_words(text):
		 
	stop_words = set(stopwords.words('portuguese')) 	  
	word_tokens = word_tokenize(text) 
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 

	return filtered_sentence

# ------------------------------------------------------------------------------

def main():

	original_text = 'falaaaa aeeeee, blz? bom #dmaissss e  fldlfmlsdsaaaaaa ae mannnooooooo'
	print('Original text: %s' % original_text)
	new_text = original_text

	# new_text = remove_URL(original_text)
	# new_text = new_text.lower()
	# new_text = remove_numbers(new_text)
	# new_text = replace_stop_words(new_text)
	# new_text = remove_punctuation(new_text)
	# new_text = TreebankWordDetokenizer().detokenize(new_text)
	new_text = remove_repeated_letters(new_text)
	new_text = remove_hashtag(new_text)
	# new_text = TreebankWordDetokenizer().detokenize(new_text)

	print('\nProcessed text: %s' % new_text)

if __name__ == '__main__':
	main()