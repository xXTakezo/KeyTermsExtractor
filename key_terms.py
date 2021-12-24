# Write your code here
from nltk import word_tokenize
from lxml import etree
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

lemmatizer = WordNetLemmatizer()

print("""
Thank you for using the Key Terms Extractor. This script will read a file and return you the n-most relevant key terms
in given text. For this, the text will be normalized and preprocessed and finally a Tf-Idf score will be calculated
for each word.
As of now, the script only accepts xml files. Please edit the xml file to have following structure:
<data>
  <corpus>
    <content>
        <value name="head">The title for your document</value>
        <value name="text">The content of the document you want to extract the key terms from</value>
    </content>
    <content>
        <value name="head">...</value>
        <value name="text">...</value>
    </content>
  </corpus>
</data>
""")

file_to_read = input('Name of the xml file: ')
n = int(input('Please input how many key terms you want to extract: '))

def open_xml(xmlfile):
    root = etree.parse(xmlfile).getroot()
    return root

def get_xml_content(xmlfile):
    all_articles = {}
    for i in range(0,(len(xmlfile[0]))):
            all_articles[xmlfile[0][i][0].text] = xmlfile[0][i][1].text #index 0 selects the title and index 1 selects the article text
    return all_articles

def process_text(dict): #given the values consists of whole sentences, this will split each word
    tokens = {}
    for key,value in dict.items():
        tokens[key] = sorted(word_tokenize(value.lower()), reverse=True)
    for key, value in tokens.items():
        tokens[key] = [lemmatizer.lemmatize(word) for word in value]
    top_words = stopwords.words('english')
    top_words.append('u')
    punctuation = string.punctuation
    for key, value in tokens.items():
        tokens[key] = [word for word in value if not word in top_words and word not in punctuation]
    for key, item in tokens.items():
            tokens[key] = [word for word in item if nltk.pos_tag([word])[0][1] == 'NN']
    return tokens

def identity_tokenizer(text):
    return text

#this function calculates the 5 highest if-idf scores for each
#text and returns it as a dictionary. finally, it outputs the terms with the highest score for each document

def tf_idf(dict):
    text = []
    for key, value in dict.items():
        text.append(value)
    tfidf = TfidfVectorizer(tokenizer=identity_tokenizer, lowercase=False)
    matrix = tfidf.fit_transform(text)
    feature_names = tfidf.get_feature_names_out()
    index = [key for key in dict.keys()]
    try:
        df_tf_idf = pd.DataFrame(matrix.T.todense(), index=feature_names, columns=index)
    except:
        pass
    df_tf_idf = df_tf_idf.sort_index(ascending=False)
    tf_idf_score_dict = {}
    for key in article_headlines:
        tf_idf_score_dict[key] = df_tf_idf[key].nlargest(n).index
    return df_tf_idf, tf_idf_score_dict


def output_highest_tfidf_scores(dict):
    for key, value in dict.items():
        print(key+':')
        print(' '.join(value), sep='')
        print('\n')


news_file = open_xml(file_to_read)

all_articles = get_xml_content(news_file) # get all articles as a dictionary with the title as key and text as value

article_headlines = []
for key in all_articles.keys():
    article_headlines.append(key)

only_nouns = process_text(all_articles)
df_tf_idf, tf_idf_score_dict = tf_idf(only_nouns)
output_highest_tfidf_scores(tf_idf_score_dict)























