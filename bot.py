import random
from webbrowser import get
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import pyttsx3

Introduce_Ans = [" "]
GREETING_INPUTS = ("hello", "hi", "hiii", "hii", "hiiii", "hiiii", "greetings", "sup", "what's up", "hey", 'Hi', 'HI')
GREETING_RESPONSES = ["Hi, Would you like some restaurent recommendations?(Y/N)", "Hey, Like some restaurent recommendations?(Y/N)"]
Basic_Q = ["yes", "y", 'Y', 'YES']
Basic_Ans = "Provide a resaturent name to find its similar ones"
Basic_Om = ["no", "n", 'N', 'No', 'thanks', 'thank you','Thanks', 'Thank You','Thank you']
Basic_AnsM = "You are Welcome! Have a great day!"

a = random.choice(GREETING_RESPONSES)
def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

df = pd.read_csv(r'C:\Users\bpavu\OneDrive\Desktop\Siri\Capstone\Zomato_Restaurent_Recommendation\data\data_topic.csv')
df['dish_reviewed'] = df['dish_reviewed'].fillna('')
df['cuisines'] = df['cuisines'].fillna('')
df['menu_item'] = df['menu_item'].fillna('')

def get_recommendations(name):

    recommended = []
    top30_list = []
    top30 = []
    name = name.lower()
    topic_num = df[df['name'].str.lower() == name].Topic.values
    doc_num = df[df['name'].str.lower() == name].Doc.values    
    output_df = df[df['Topic']==topic_num[0]].sort_values('Probability', ascending=False).reset_index(drop=True)
    
    
    cols = ['name','location', 'rest_type', 'rest_type', 'rest_type', 'cuisines', 'dish_reviewed', 'menu_item', 'online', 'table_booking','listed_as', 'listed_in_city']
    
    output_df['combined'] = output_df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    
    # Creating tf-idf matrix
    tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(output_df['combined'])
    
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    scores_df = pd.DataFrame(cosine_similarities)

    index = output_df[output_df['Doc']==doc_num[0]].index[0]
    
    top30_list = list(scores_df.iloc[index].sort_values(ascending = False).iloc[1:31].index)
    
    for each in top30_list:
        if output_df.iloc[each]['name'].lower() != name:
            top30.append(output_df.iloc[each]['name'])
        
    a = [x.lower() for x in top30]

    filtered = output_df[output_df['name'].str.lower().isin(a)]
    filtered_sorted = filtered.sort_values("weighted_rating",ascending=False)
    
    for i in filtered_sorted['name']:
        if recommended.count(i) <= 0:
            recommended.append(i)
        if len(recommended) == 10:
            break

    return recommended



def chat(user_response):
    global resp
    flag = True
    found = 0
    engine = pyttsx3.init()
    engine.setProperty('volume',1.0)
    # engine.say(user_response)
    engine.runAndWait()
    engine.stop()
    if (user_response in GREETING_INPUTS):    
        return a
    elif (user_response in Basic_Q):
        return Basic_Ans
    elif ((user_response not in GREETING_INPUTS) and (user_response not in Basic_Q) and (user_response not in Basic_Om)):
        for i in range(len(df['name'])):
            if df['name'][i] == user_response:
                found = 1
                print(found) 
        if found == 1:
            print(str(get_recommendations(user_response)))
            final_list = ''
            p = get_recommendations(user_response)
            for i in p:
                final_list = final_list + str(i) + '<br>'
            return final_list

        else:
            return 'I dont understand would you like to try again(Y/N)' 
    elif (user_response in Basic_Om):
        return Basic_AnsM