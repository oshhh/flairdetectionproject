from flask import Flask, request, render_template
from praw import Reddit
from praw.models import Submission
import nltk
nltk.download('wordnet')

app = Flask(__name__)

reddit = Reddit(client_id='s1AWAyUUUL0GpA',
                     client_secret="mwFF5IMVIZfJSXi_JeaD68HtBDY", password='saumya@ths',
                     user_agent='myapp_oshhh_', username='_oshhh_')

@app.route('/', methods=['GET'])
def get_homepage():
    return render_template('homepage.html')

@app.route('/', methods=['POST'])
def get_resultpage():
    text = request.form['Link']
    predicted_flair, real_flair = getFlair(text)
    return render_template('resultpage.html', predicted_flair = predicted_flair, real_flair = real_flair)

@app.route('/dataanalysis', methods=['GET'])
def get_dataanalysis():
    return render_template('dataanalysis.html')

@app.route('/model', methods=['GET'])
def get_model():
    return render_template('model.html')

@app.route('/modelv2', methods=['GET'])
def get_model_v2():
    return render_template('modelv2.html')


def cleanup(text):
    text = text.lower()
    text = re.sub(r'@\S+', '', text) # remove mentions
    text = re.sub(r'(www\.\S+)|(https?\://\S+)', '', text) # remove urls
    text = re.sub(r'#(\S+)', r'\1', text) # replaces #hashtag with hashtag
    text = re.sub(r'\brt\b', '', text) # remove RT
    text = re.sub(r'\'s', '', text) # remove possession apostrophe
    text = re.sub(r"n\'t", " not", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'t", " not", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'m", " am", text)
    text = re.sub(r'(\.{2,})|(\s+)', ' ', text) # replace 2+ dots/spaces with a single space
    text = re.sub(r'[^A-Za-z0-9]+', ' ', text) # remove non-alphanumeric chars (punctuations also removed)
    text = re.sub(r'(.)\1+', r'\1\1', text) # replace repeated char seq of length >=2 with seq of length 2
    return text

import re
import string
import nltk
from nltk.tokenize.casual import _replace_html_entities
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import string
from nltk.stem import WordNetLemmatizer
from joblib import load

punctuations = string.punctuation
lemmatizer = WordNetLemmatizer()
clf = load('model.joblib') 

def preprocess(sentence):
    if str(sentence) == None:
        return ''
    sentence = cleanup(sentence)
    sentence = ''.join(j for j in sentence if j not in punctuations)
    sentence = ' '.join(lemmatizer.lemmatize(j.lower()) for j in sentence.split())
    return sentence


def getFlair(text):
	sub = Submission(reddit, url = text)
	flair = sub.link_flair_text
	if flair == None:
		flair = 'None'
	title = sub.title
	body = sub.selftext
	all_text = preprocess(title) + ' ' + preprocess(body)
	prediction = clf.predict([all_text])
	predicted_flair = None
	flairs = ['AskIndia', 'Business/Finance', 'Food', 'Photography', 'Policy/Economy', 'Politics', 'Science/Technology', 'Sports', '[R]eddiquette']
	return flairs[prediction[0]], flair

if __name__ == '__main__':
    app.run()
