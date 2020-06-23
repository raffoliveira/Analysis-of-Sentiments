import json

#--------------------------------------------------------------------------------------
def generating_texts(profile_id):

    destination_path = '/home/rafael/TCC_II/coleta_TCC_II/coletas'
    months = ['agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    path_file = 'comments_total_processed_without_stop_words_sentiment'
    file_full = 'text_word_cloud_todos.txt'
            
    for id_months in months:
        
        file_r = '%s/%s/%s/comments/%s.json' % (destination_path, profile_id, id_months, path_file)
        file_w = 'text_word_cloud_%s.txt' % (id_months) 
        text_join = []        

        with open(file_r, 'r') as file_read:			

            for line in file_read:

                list_of_comments = json.loads(line)['comments']

                for id_comments in list_of_comments:

                    message = id_comments['message']
                    text_join.append(message)

        text_full = ' '.join(text_join)

        with open(file_w, 'w') as file:
            file.write(text_full)

        with open(file_full, 'at') as file:
            file.write(text_full)

#--------------------------------------------------------------------------------------
def main():

    profiles = ['bolsonaro', 'haddad']	
    generating_texts(profiles[1])

if __name__ == '__main__':
    main()