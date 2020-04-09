from functools import lru_cache
#lru_cache =  least recently use cache

# fibonnaci_cache = {}

@lru_cache(maxsize = 1000)
def fibonnaci(input_value):
	if input_value == 1 or input_value == 2:
		return 1
	if input_value > 2:
		return fibonnaci(input_value - 1) + fibonnaci(input_value - 2)

def fibonnaci_memo(input_value):

	if input_value in fibonnaci_cache:
		return fibonnaci_cache[input_value]
	elif input_value == 1 or input_value == 2:
		value = 1
	elif input_value > 2:
		value = fibonnaci_memo(input_value - 1) + fibonnaci_memo(input_value - 2)
	
	fibonnaci_cache[input_value] = value

	return value

def main():

	for i in range(1,2001):
		print('fib({}) = '.format(i), fibonnaci(i))

if __name__ == '__main__':
	main()
