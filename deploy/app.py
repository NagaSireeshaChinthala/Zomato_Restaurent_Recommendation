import streamlit as st
import pandas as pd 
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

st.title("Restuarant Recommendation System")
#st.image("foood.jpg")

df = pd.read_csv("data/data_topic.csv")

df['dish_reviewed'] = df['dish_reviewed'].fillna('')
df['cuisines'] = df['cuisines'].fillna('')
df['menu_item'] = df['menu_item'].fillna('')

st.subheader("Location")
loc = ['No Selection']
a = df['location'].sort_values(ascending=True).unique().tolist()
loc.extend(a)

location = st.selectbox("Choose your favourite!",loc)


st.subheader("Cost For Two people?")


cost = st.slider("from low to high!",min_value=0,max_value = 6000, value=6000)


st.subheader("Minimum Rating?")  #RATING
rating = st.slider("from poor to the best!",min_value=0,max_value = 5, value=0)

st.subheader("Select a restaurant name to find its similar ones")
name = ['No Selection']
c = df['name'].sort_values(ascending=True).unique().tolist()
name.extend(c)

restuarant_name = st.selectbox("Choose your favourite!",name)

def get_recommendations(location,rating,cost,name = restuarant_name):
    try:
        recommended = []
        top30_list = []
        top30 = []
        print(location)
        if name != 'No Selection':
            print(name)
            name = name.lower()
            topic_num = df[df['name'].str.lower() == name].Topic.values
            doc_num = df[df['name'].str.lower() == name].Doc.values  
            #print(doc_num)  
            output_df = df[df['Topic']==topic_num[0]].sort_values('Probability', ascending=False).reset_index(drop=True)
        else:
            output_df = df

        print(len(output_df))

        if location != 'No Selection' and name == 'No Selection':
            output_df = output_df[output_df['location'].str.lower() == location.lower()]

        print(len(output_df))

        output_df = output_df[output_df['cost_for_two'] <= cost]

        print(len(output_df))

        output_df = output_df[output_df['weighted_rating'] >= rating]

        print(len(output_df))

        output_df = output_df.reset_index(drop=True)

        
        if name != 'No Selection':  
            doc_num = output_df[output_df['name'].str.lower() == name].Doc.values  
            cols = ['name','location', 'rest_type', 'rest_type', 'rest_type', 'cuisines', 'dish_reviewed', 'menu_item', 'online', 'table_booking','listed_as', 'listed_in_city']
        
            output_df['combined'] = output_df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        
            # Creating tf-idf matrix
            tfidf = TfidfVectorizer()
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

        else:
            filtered_sorted = output_df.sort_values("weighted_rating",ascending=False)
        
            for i in filtered_sorted['name']:
                if recommended.count(i) <= 0:
                    recommended.append(i)
                if len(recommended) == 10:
                    break

        return recommended
    except:
        return ['No Matching Restaurants Found']


display = get_recommendations(location,rating,cost,restuarant_name)

for i in display:
    st.write(i)