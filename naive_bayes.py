import numpy as np
import re
import clean_txt

train_data,train_label=np.load("data_train.pkl/data_train.pkl",allow_pickle=True)
test_data=np.load("data_test.pkl/data_test.pkl",allow_pickle=True)

from sklearn.model_selection import train_test_split
np.random.seed(0)
# indices = np.random.permutation(len(train_label))
(train_data_x, test_data_x, 
 train_data_y, test_data_y) = train_test_split(train_data[0:-6000], train_label[0:-6000], test_size=10000) # 


labels = ['anime', 'nfl', 'soccer', 'canada', 'Overwatch', 'leagueoflegends', 'europe', 'worldnews', 'wow', 'Music', 'nba', 'funny', 'movies', 'baseball', 'hockey', 'GlobalOffensive', 'trees', 'gameofthrones', 'conspiracy', 'AskReddit']




import scipy.sparse as sp
import nltk
from nltk.stem import SnowballStemmer
snowball_stemmer = SnowballStemmer('english')
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))

my_special_word_list = {"first","also","","yeah", "s", "much", "one", "two", "day", "els","de","b","r","f6"}

new_stop_words = set.union(stopWords, my_special_word_list)
def get_para_from_text(text): 
    
    cleaned_para_list = []
    for para in text:
        para = clean_txt.pre_process(para)
        para = re.sub("[^0-9a-zA-Z]+", " ", para).strip() #removing special characters
        # para = re.sub("[0-9]*", "", para).strip()
        cleaned_para_list.append(para)
    return cleaned_para_list

def get_features_from_para(para):
    feature_list = []
    for word in para.split(" "):
        word = snowball_stemmer.stem(word)
        if word not in new_stop_words and len(word)>2:
            feature_list.append(word) 
    return feature_list




from collections import Counter

def get_feature_prob_in_each_para(para, BoW):
    dict_count = Counter(get_features_from_para(para))
    for key, value in dict_count.items():
        if key in BoW:
            BoW[key] = value 
    return list(BoW.values())

def data_processing(raw_data_x):
    cleaned_data_set = get_para_from_text(raw_data_x)
    features = []
    for para in cleaned_data_set:

        
        feature_list = get_features_from_para(para) # Get features from each para 
        features.extend(feature_list)
    features = list(dict.fromkeys(features))
    BoW = dict.fromkeys(features, 0)
    cleaned_data_x = []
    for para in cleaned_data_set:
        BoW = dict.fromkeys(features, 0)
        feature_count = get_feature_prob_in_each_para(para, BoW) 
        cleaned_data_x.append(feature_count)
    return cleaned_data_x, features

cleaned_data_with_feature_count, features = data_processing(train_data_x)
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(cleaned_data_with_feature_count, train_data_y)
clf.predict(cleaned_data_with_feature_count)
clf.predict_proba(cleaned_data_with_feature_count)  
print(clf.score(cleaned_data_with_feature_count, train_data_y))

def data_processing_for_test_data(raw_data_x, features):
    cleaned_data_set = get_para_from_text(raw_data_x)
    cleaned_data_x = []
    for para in cleaned_data_set:
        BoW = dict.fromkeys(features, 0)
        feature_count = get_feature_prob_in_each_para(para, BoW) 
        cleaned_data_x.append(feature_count)
    return cleaned_data_x


cleaned_test_data_x = data_processing_for_test_data(test_data_x, features)
print(clf.score(cleaned_test_data_x, test_data_y))
# test_data_x