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


file_format = input('Please specify the file format."xml" for a single xml file or "txt" for one or a series of txt files: ')
def handle_input():
    list_of_textfiles = []
    if file_format == 'txt':
        print("""
        You selected the txt file format. For this, use the first line of the txt file as the headline and the rest 
        of the file as the content from which you want to extract the key terms. Example format:
        Line 1..........HEADER
        Line 2..........CONTENT
        Line 3..........CONTENT
        [....]
        """)
        for i in range(100):
            document = input('Please specify the name of your ' + str(i+1) +'. file: ')
            list_of_textfiles.append(open(document, 'r'))
            more_files = input('File has been saved to the list of documents. Do you wish to add more files?(y,n) ')
            if more_files == 'y':
                pass
            elif more_files == 'n':
                break
        corpus = {}
        for document in list_of_textfiles:
            lines = document.read()
            corpus[lines.split('\n',1)[0]] = ' '.join(lines.split('\n')[1:])
            document.close()
        return corpus
    elif file_format == 'xml':
        print("""
        Please edit the xml file to have following structure:
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
        root = etree.parse(file_to_read).getroot()
        all_articles = {}
        for i in range(0,(len(root[0]))):
            all_articles[root[0][i][0].text] = root[0][i][1].text
        return all_articles


n = int(input('How many Key Terms do you want to extract? '))


def process_text(dict): #process the text by tokenizing, lemmatizing as well as removing stop words, punctuation marks and non noun words
    tokens = {}
    for key,value in dict.items():
        tokens[key] = sorted(word_tokenize(value.lower()), reverse=True)
    for key, value in tokens.items():
        tokens[key] = [lemmatizer.lemmatize(word) for word in value]
    top_words = stopwords.words('english')
    top_words = top_words + ['ha', 'wa', 'u', 'a', 'tm']
    punctuation = string.punctuation
    for key, value in tokens.items():
        tokens[key] = [word for word in value if not word in top_words and word not in punctuation]
    for key, item in tokens.items():
            tokens[key] = [word for word in item if nltk.pos_tag([word])[0][1] == 'NN']
    return tokens

def identity_tokenizer(text):
    return text

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
    tf_idf_score_dict_all = {}
    for key in article_headlines:
        tf_idf_score_dict[key] = df_tf_idf[key].nlargest(n).index
        tf_idf_score_dict_all[key] = df_tf_idf[key].nlargest(n)
    return df_tf_idf, tf_idf_score_dict,tf_idf_score_dict_all


def output_highest_tfidf_scores(dict,dict_two):# only show terms without their tfidf score
    key_terms = open('key_terms.txt','w')
    for (k,v),(k2,v2) in zip(dict.items(),dict_two.items()):
        key_terms.write('Key Terms in descending order for: '+k)
        print('Key Terms in descending order for: '+k)
        key_terms.write('\n')
        key_terms.write(' - '.join(v))
        print(' - '.join(v))
        key_terms.write('\n')
        print('\n')
        key_terms.write(str(v2))
        print(v2)
        key_terms.write('\n')
        print('\n')
    key_terms.close()

dataset = handle_input()

article_headlines = []
for key in dataset.keys():
    article_headlines.append(key)
processed_dataset = process_text(dataset)
df_tf_idf, tf_idf_score_dict,tf_idf_score_dict_all = tf_idf(processed_dataset)
output_highest_tfidf_scores(tf_idf_score_dict, tf_idf_score_dict_all)


























