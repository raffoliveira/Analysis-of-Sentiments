# -*- coding: utf-8 -*-

import time, gzip, json, requests, facebook, logging
from time import sleep, strftime
from datetime import datetime
from facebookads.exceptions import FacebookError
from requests.exceptions import HTTPError

token = 'EAAbPAyrnxo0BABIJEQDEostbMXrSbsCpdpKCg79JZC0XhWBNZAcaHEGNLmAoLasK6LcCWopsvjwVX794A7wZApm6ycNBNwxTlTJZB22QBNWn6VW1f7nDZBP5wQJ4EhbMY6S4lPDQ3K15ahBDbcwzuu9JBrbdPf1g6Dvw8RU49FgZDZD'

graph = facebook.GraphAPI(access_token = token, version = 3.1)

#===========================================================================

def get_current_time():
	return '%s' % (time.strftime("%Y-%m-%d--%H-%M-%S")) 

#===========================================================================
#converter uma data em unixtimestamp

def convertDateInUnixTimeStamp(stime):
	return '%s' % (datetime.strptime(stime, "%Y-%m-%dT%H:%M:%S+0000").timestamp())

#===========================================================================
#converter unixtimestamp em data

def convertUnixTimeStampInDate(stime):
	return '%s' % (datetime.utcfromtimestamp(stime).strftime('%Y-%m-%dT%H:%M:%S+0000'))


#===========================================================================
#checa o limite do FB rate limit

def check_limit(url_check, log_file):

	if 'x-app-usage' in url_check.headers:

		call = json.loads(url_check.headers['x-app-usage'])['call_count']
		cpu = json.loads(url_check.headers['x-app-usage'])['total_cputime']
		total = json.loads(url_check.headers['x-app-usage'])['total_time']

		log_file.write('\nCurrent Usage: CALL_COUNT: {call}, TOTAL_CPUTIME: {cpu}, TOTAL_TIME: {total}'.format(call=call, cpu=cpu, total=total))
	else:
		return 0 

	return max(call, cpu, total)

#===========================================================================
#request de post

def makeGraphRequest(req, exception_log):

	graph_response = False
	result_fetched = True
	count_total_requests = 0
	exception_counter = 0
	time_sleep = 0
	
	while result_fetched:
		if exception_counter == 5:
			exception_log.write('\n<<<<<<<< TEN EXCEPTIONS - REQUEST ABORTED >>>>>>>>>\n') 
			return None  
		try:                      
			graph_response = graph.request(req) 
			result_fetched = False
			
		except FacebookError as error:
			exception_counter += 1
			count_total_requests += 1

			try:
				exception_log.write('<<<<<<<< Exception >>>>>>>>>\n')
				exception_log.write('\t#Total of requests: %d\n' % count_total_requests)                                                 
				exception_log.write('\terror_type: %s\n' % error.api_error_type())
				exception_log.write('\terror_code: %d\n' % error.api_error_code())
				exception_log.write('\terror_subcode: %d\n' % error.api_error_subcode())
				exception_log.write('\terror_message: %s\n' % error.api_error_message())     
				exception_log.flush()
			except:
				exception_log.write('\nlog_failed: %d \n' % count_total_requests)
				exception_log.flush()

			if exception_counter == 1:
				time_sleep = (5 * 60)

			if error.api_error_message() == 'An unknown error occurred':
				time_sleep = (5 * 60) * exception_counter
				exception_log.write('\nAn unknown error occurred')
				exception_log.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60)) 	

			else:
				time_sleep = (5 * 60) * exception_counter
				exception_log.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60)) 
			
			sleep(time_sleep)

		except facebook.GraphAPIError as error: 
			exception_counter += 1
			exception_log.write('\nError found: %s\n' % error)			
			time_sleep = (5 * 60) * exception_counter
			exception_log.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60)) 
			exception_log.flush()

			sleep(time_sleep)

		# except: 
		# 	count_total_requests += 1
		# 	exception_counter += 1
		# 	exception_log.write('\n<<<<<<<< REGULAR Exception >>>>>>>>>\n')
		# 	exception_log.write('\n# exceptions: %d\n' % exception_counter)
		# 	time_sleep = (5 * 60) * exception_counter
		# 	exception_log.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60))  
		# 	exception_log.flush()

		# 	sleep(time_sleep)                        
			
	return graph_response

#===========================================================================
#escrita em arquivo

def writeInFile(file, content):

	file.write('%s\n' % json.dumps(content))

#===========================================================================
#paginação comentarios

def getPublicCommentsFromID(facebook_id, exception_log):

	comments_content = [] #recebe os comentarios de cada post
	collected_comments = set([])
	count_error = 0
	time_sleep = 0
	timer_paging = 0
	
	d_begin = 1
	d_end = 2

	while (d_end <= 31):

		begin = "2018-12-%d" % d_begin
		end = "2018-12-%d" % d_end

		outFile_comments_posts = gzip.open('posts_comments_haddad_' + str(begin) + '_' + str(end) + '_' + '.json.gz', 'wt')

		with gzip.GzipFile('posts_all_haddad_' + str(begin) + '_' + str(end) + '_' + '.json.gz', 'r') as file:

			for line in file:
				
				line = line.strip()
				obj = json.loads(line)
				post_id = obj['id']	

				posts_request = str(post_id) + '/comments?limit=300&fields=created_time,id,message,comment_count'

				commentsPosts = makeGraphRequest(posts_request, exception_log)

				if commentsPosts == None:
					exception_log.write('Response is null.')
					return

				while(True):

					if 'data' in commentsPosts:

						for comments_id in commentsPosts['data']:

							if comments_id['id'].strip() not in collected_comments:

								collected_comments.add(comments_id['id'].strip())
								comments_content += [comments_id]
							else:
								continue

						if 'paging' in commentsPosts:
							
							if 'next' in commentsPosts['paging']:

								try:
									checkCommentsPosts = requests.get(commentsPosts['paging']['next'])
									print('\nheaders_comments\n')
									print(checkCommentsPosts.headers)
									commentsPosts = checkCommentsPosts.json()
									timer_paging += 1
															
								except FacebookError as error:

									count_error += 1
									
									try:
										exception_log.write('<<<<<<<< Exception in comments>>>>>>>>>\n')
										exception_log.write('\terror_type: %s\n' % error.api_error_type())
										exception_log.write('\terror_code: %s\n' % error.api_error_code())
										exception_log.write('\terror_subcode: %s\n' % error.api_error_subcode())
										exception_log.write('\terror_message: %s\n' % error.api_error_message())     
										exception_log.flush()
									except:
										exception_log.write('\tlog_failed: %d \n' % count_total_requests)
										exception_log.flush()

									if count_error == 1:
										time_sleep = (5 * 60)

									if error.api_error_message() == 'An unknown error occurred':
										time_sleep = (5 * 60) * count_error
										exception_log.write('\nAn unknown error occurred')
										exception_log.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60)) 	

									else:
										time_sleep = (5 * 60) * count_error
										exception_log.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60)) 
									
									sleep(time_sleep)

								except HTTPError as http_err:
									count_error += 1
									time_sleep = (5 * 60) * count_error
									exception_log.write('\nHTTP error occurred: {http_err}'.format(http_err=http_err))
									sleep(time_sleep)
									
								except Exception as err:
									count_error += 1
									time_sleep = (5 * 60) * count_error
									exception_log.write('\nOther error occurred: {err}'.format(err=err)) 
									sleep(time_sleep) 

								except:
									exception_log.write('<<<<<<<< Regular Exception in comments >>>>>>>>>\n')
									exception_log.write('\t# exceptions: %d\n' % count_error)
									count_error += 1
									time_sleep = (5 * 60) * count_error
									exception_log.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60))  
									exception_log.flush()   
									sleep(time_sleep)

								if (check_limit(checkCommentsPosts, exception_log) > 70):

									count_error += 1
									time_sleep = (10 * 60) * count_error
									exception_log.write('\n70% Rate Limit Reached. Cooling Time %.2lf minutes' % (float(time_sleep)/60))
									logging.debug('\n70% Rate Limit Reached. Cooling Time 10 Minutes.')
									sleep(time_sleep)

								if 'WWW-Authenticate' in checkCommentsPosts.headers:
									break				
									
							else:
								break
						else:
							break

						if (timer_paging % 20) == 0:
							sleep(5*60)

					else:		
						continue	

				item = {'id_post': post_id, 'comments': comments_content}
				writeInFile(outFile_comments_posts, item)
				comments_content = []
				timer_paging = 0
				sleep(5*60)

		file.close()
		outFile_comments_posts.close()
		d_begin += 1
		d_end += 1

#===========================================================================
#paginação dos posts

def pagingPosts(required_posts, collected_posts, file_all_posts, file_ids_posts, log_file):

	count_error = 0
	time_sleep = 0

	while(True):

		if 'data' in required_posts:			

			for post_id in required_posts['data']:

				if post_id['id'].strip() not in collected_posts:

					collected_posts.add(post_id['id'].strip())
					idEveryPost = {'id_post': post_id['id'], 'created_time': post_id['created_time']}
					writeInFile(file_ids_posts, idEveryPost)   #escreve o id de cada post
					writeInFile(file_all_posts, post_id)       #escreve o post todo

				else:
					continue

			if 'paging' in required_posts:
					
				if 'next' in required_posts['paging']:

					try:
						checkRequired_posts = requests.get(required_posts['paging']['next'])
						print('\nheaders_post\n')
						print(checkRequired_posts.headers)
						required_posts = checkRequired_posts.json()
											
					except FacebookError as error:

						count_error += 1
						
						try:
							log_file.write('<<<<<<<< Exception in comments>>>>>>>>>\n')
							log_file.write('\terror_type: %s\n' % error.api_error_type())
							log_file.write('\terror_code: %s\n' % error.api_error_code())
							log_file.write('\terror_subcode: %s\n' % error.api_error_subcode())
							log_file.write('\terror_message: %s\n' % error.api_error_message())     
							log_file.flush()
						except:
							log_file.write('\tlog_failed: %d \n' % count_total_requests)
							log_file.flush()

						if count_error == 1:
							time_sleep = (5 * 60)

						if error.api_error_message() == 'An unknown error occurred':
							time_sleep = (5 * 60) * count_error
							log_file.write('\nAn unknown error occurred')
							log_file.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60)) 	

						else:
							time_sleep = (5 * 60) * count_error
							log_file.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60)) 
						
						sleep(time_sleep)

					except HTTPError as http_err:
						count_error += 1
						time_sleep = (5 * 60) * count_error
						log_file.write('\nHTTP error occurred: {http_err}'.format(http_err=http_err))
						sleep(time_sleep)
						
					except Exception as err:
						count_error += 1
						time_sleep = (5 * 60) * count_error
						log_file.write('\nOther error occurred: {err}'.format(err=err)) 
						sleep(time_sleep) 

					except:
						log_file.write('<<<<<<<< Regular Exception in comments >>>>>>>>>\n')
						log_file.write('\t# exceptions: %d\n' % count_error)
						count_error += 1
						time_sleep = (5 * 60) * count_error
						log_file.write('\nWaiting %.2lf minutes to restart again...' % (float(time_sleep)/60))  
						log_file.flush()   
						sleep(time_sleep)

					if (check_limit(checkRequired_posts, log_file) > 70):

						count_error += 1
						time_sleep = (5 * 60) * count_error
						log_file.write('\n70% Rate Limit Reached. Cooling Time %.2lf minutes' % (float(time_sleep)/60))
						logging.debug('\n70% Rate Limit Reached. Cooling Time 10 Minutes.')
						sleep(time_sleep)			
					
				else:
					break
			else:
				break			
		else:
			break

#===========================================================================
#chamada do resquest e paginações

def getPublicPostFromID(facebook_id, log_file, begin, end):

	collected_posts = set([])

	outFile_all_posts = gzip.open('posts_all_haddad_' + str(begin) + '_' + str(end) + '_' + '.json.gz', 'wt')
	outFile_ids_posts = gzip.open('posts_ids_haddad_' + str(begin) + '_' + str(end) + '_' + '.json.gz', 'wt')
	
	# outFile_all_posts = gzip.open('posts_all_' + str(facebook_id) +  '.json.gz','at')
	# outFile_ids_posts = gzip.open('posts_ids_' + str(facebook_id) + '.json.gz','at')

	post_request = str(facebook_id) + '/posts?since=%s&until=%s&\
	filter=stream&limit=50&fields=created_time,id,message,shares,status_type,full_picture,\
	reactions.type(LIKE).limit(0).summary(total_count).as(reactions_like),\
	reactions.type(HAHA).limit(0).summary(total_count).as(reactions_haha),\
	reactions.type(WOW).limit(0).summary(total_count).as(reactions_wow), \
	reactions.type(SAD).limit(0).summary(total_count).as(reactions_sad),\
	reactions.type(ANGRY).limit(0).summary(total_count).as(reactions_angry),\
	reactions.type(LOVE).limit(0).summary(total_count).as(reactions_love)' % (begin, end)

	response = makeGraphRequest(post_request, log_file)

	if response == None:
		log_file.write('Response is null.\n')
		exit()

	if 'data' not in response:
		log_file.write('Response doesn\'t have data.\n')
		outFile_all_posts.close()
		outFile_ids_posts.close()
		return

	if response['data'] == []:
		log_file.write('Response data in %s to %s is empty.\n' % (begin, end))
		outFile_all_posts.close()
		outFile_ids_posts.close()
		return
		
	print(response)

	pagingPosts(response, collected_posts, outFile_all_posts, outFile_ids_posts, log_file)

	outFile_all_posts.close()
	outFile_ids_posts.close()
	
#===========================================================================  
	
def main():

	log_file = open('log.txt', 'w')

	facebook_ids = ['211857482296579', '904277726319518', '1216504185136925', '353551475083023']

	# 0 -> bolsonaro
	# 1 -> fernando haddad
	# 2 -> ciro gomes
	# 3 -> joao amoedo (Novo)

	face_id = facebook_ids[0]

	d_begin = 1
	d_end = 2

	while (d_end <= 31):

		begin = "2018-12-%d" % d_begin
		end = "2018-12-%d" % d_end

		getPublicPostFromID(face_id, log_file, begin, end)
		sleep(3*60)     	
		d_begin += 1
		d_end += 1

	getPublicCommentsFromID(face_id, log_file)
	
if __name__ == "__main__":   
	main()

