import pandas as pd
import pymysql
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import json




def func(x):
    conn = pymysql.connect(host="localhost",user="root",password="",database="ead")
    cursor = conn.cursor()


    retrieve = f"Select cus_ID from customers where email = '{x}';"

    cursor.execute(retrieve)

    rows = cursor.fetchall()
    id = rows[0][0]


    retrieve2 = "Select * from movies;"
    cmd2 = f"SELECT movie from screens WHERE screen_Id in (SELECT screen_id FROM booked WHERE cust_id={id} Order by Date DESC);"

    cursor.execute(retrieve2)
    rows = cursor.fetchall()

    cursor.execute(cmd2)
    rows2 = cursor.fetchall()
    rows2 = rows2[:5]

    df = pd.DataFrame(list(rows),columns=['title','rating','year','genre','poster','plot','actors','runtime','embedcode'])
    df.drop(df[df['plot']=='N/A'].index, inplace = True)
    df.reset_index(inplace = True)




    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')

    matrix = tf.fit_transform(df['genre'])
    matrix2 = tf.fit_transform(df['plot'])




    cosine_similarities = linear_kernel(matrix,matrix)
    cosine_similarities2 = linear_kernel(matrix2,matrix2)


    movie_title = df['title']

    indices = pd.Series(df.index, index=df['title'])


    def movie_recommend(rows2):
        idx = indices[rows2[0][0]]
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores2 = list(enumerate(cosine_similarities2[idx]))
        sim_scores = sim_scores+sim_scores2
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:10]

        for i in range(1,len(rows2)):
            idx = indices[rows2[i][0]]
            sim_scorestemp = list(enumerate(cosine_similarities[idx]))
            sim_scores2temp = list(enumerate(cosine_similarities2[idx]))
            sim_scorestemp = sim_scorestemp+sim_scores2temp
            sim_scorestemp = sorted(sim_scorestemp, key=lambda x: x[1], reverse=True)

            sim_scorestemp = sim_scorestemp[1:10]
            sim_scores+=sim_scorestemp
            movie_indices = [i[0] for i in sim_scores]

            return movie_title.iloc[movie_indices]





    recommended_movies = list(movie_recommend(rows2)[0:10])

    df = df.set_index('title')
    picpaths = []
    for movie in recommended_movies:
        picpaths.append(df.loc[movie]['poster'])

    # output = ''
    # for movie in recommended_movies:
    #     output += movie+','
    D = {'foo':recommended_movies,'doo':picpaths}

    return json.dumps(D)








# conn = pymysql.connect(host="localhost",user="root",password="",database="ead")
# cursor = conn.cursor()
#
#
# retrieve = f"Select cus_ID from customers where email = '{x}';"
#
# cursor.execute(retrieve)
#
# rows = cursor.fetchall()
# id = rows[0][0]
#
#
# retrieve2 = "Select * from movies;"
# cmd2 = f"SELECT movie from screens WHERE screen_Id in (SELECT screen_id FROM booked WHERE cust_id={id} Order by Date DESC);"
#
# cursor.execute(retrieve2)
# rows = cursor.fetchall()
#
# cursor.execute(cmd2)
# rows2 = cursor.fetchall()
# rows2 = rows2[:5]
#
# df = pd.DataFrame(list(rows),columns=['title','rating','year','genre','poster','plot','actors','runtime','embedcode'])
# df.drop(df[df['plot']=='N/A'].index, inplace = True)
# df.reset_index(inplace = True)
#
#
# from sklearn.feature_extraction.text import TfidfVectorizer
#
# tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
#
# matrix = tf.fit_transform(df['genre'])
# matrix2 = tf.fit_transform(df['plot'])
#
#
# from sklearn.metrics.pairwise import linear_kernel
#
# cosine_similarities = linear_kernel(matrix,matrix)
# cosine_similarities2 = linear_kernel(matrix2,matrix2)
#
#
# movie_title = df['title']
#
# indices = pd.Series(df.index, index=df['title'])
#
#
# def movie_recommend(rows2):
#    idx = indices[rows2[0][0]]
#    sim_scores = list(enumerate(cosine_similarities[idx]))
#    sim_scores2 = list(enumerate(cosine_similarities2[idx]))
#    sim_scores = sim_scores+sim_scores2
#    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#    sim_scores = sim_scores[1:10]
#    for i in range(1,len(rows2)):
#        idx = indices[rows2[i][0]]
#        sim_scorestemp = list(enumerate(cosine_similarities[idx]))
#        sim_scores2temp = list(enumerate(cosine_similarities2[idx]))
#        sim_scorestemp = sim_scorestemp+sim_scores2temp
#        sim_scorestemp = sorted(sim_scorestemp, key=lambda x: x[1], reverse=True)
#
#        sim_scorestemp = sim_scorestemp[1:10]
#        sim_scores+=sim_scorestemp
#        movie_indices = [i[0] for i in sim_scores]
#        return movie_title.iloc[movie_indices]
#
#
# recommended_movies = list(movie_recommend(rows2)[0:10])
#
# output = ''
# for movie in recommended_movies:
#    output += movie+','
# print(output[:-1])
