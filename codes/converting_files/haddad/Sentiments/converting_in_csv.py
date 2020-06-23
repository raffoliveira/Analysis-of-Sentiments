import csv, json

#--------------------------------------------------------------------------------------
def converting_files(profile_id):

    destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
    months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    path_file = ['comments_total',
                 'comments_total_sentiment', 
                 'comments_total_processed_with_stop_words',                 
                 'comments_total_processed_with_stop_words_sentiment',
                 'comments_total_processed_without_stop_words',
                 'comments_total_processed_without_stop_words_sentiment']
        
    for j, id_path_file in enumerate(path_file):

        file_w = '%s.csv' % (id_path_file)

        if j%2 != 0:
            data_comments = [['ID_post', 'Created_time', 'ID_comment', 'Message', 'Replies_count', 'Sentiment_dual',
                            'Sentiment_binary', 'Sentimental_trinary', 'Sentiment_scale']]
        else: 
            data_comments = [['ID_post', 'Created_time', 'ID_comment', 'Message', 'Replies_count']]   
            
        for id_months in months:           

            file_r = '%s/%s/%s/comments/%s.json' % (destination_path, profile_id, id_months, id_path_file)           

            with open(file_r, 'r') as file_read:			

                for line in file_read:

                    id_post = json.loads(line)['id_post']
                    list_of_comments = json.loads(line)['comments']

                    if j%2 != 0:

                        for id_comments in list_of_comments:

                            created_time = id_comments['created_time']
                            id_comment = id_comments['id']
                            message = id_comments['message']
                            replies_count = id_comments['comment_count']

                            if id_comments['sentiment_scores'] != {}:

                                sentiment_dual = id_comments['sentiment_scores']['dual'][0]
                                sentiment_binary = id_comments['sentiment_scores']['binary'][0]
                                sentiment_trinary = id_comments['sentiment_scores']['trinary'][0]
                                sentiment_scale = id_comments['sentiment_scores']['scale'][0] 
                            else:
                                sentiment_dual = 0
                                sentiment_binary = 0
                                sentiment_trinary = 0
                                sentiment_scale = 0

                            data_comments.append([id_post, created_time, id_comment, message, replies_count, sentiment_dual,
                                                sentiment_binary, sentiment_trinary, sentiment_scale])
                    else:

                        for id_comments in list_of_comments:
                            
                            created_time = id_comments['created_time']
                            id_comment = id_comments['id']
                            message = id_comments['message']
                            replies_count = id_comments['comment_count']
                   
                            data_comments.append([id_post, created_time, id_comment, message, replies_count])

        with open(file_w, 'w') as file_write:
            writer = csv.writer(file_write, delimiter = '\t')
            writer.writerows(data_comments)

        data_comments = []


#--------------------------------------------------------------------------------------
def main():

    profiles = ['bolsonaro', 'haddad']	
    converting_files(profiles[0])

if __name__ == '__main__':
    main()