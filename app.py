from flask import Flask, request, render_template
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model

print(tf.__version__)
app = Flask(__name__)
sentiment = load_model('C:/Users/vivek/Desktop/NLP Project/sentiment_analysis.h5')

@app.route('/')
def main():
    return render_template("index.html", output="this is output")

@app.route('/predict',methods=['POST'])

def clean_text(text, remove_stopwords = True):
    '''Remove unwanted characters, stopwords, and format the text to create fewer nulls word embeddings'''
    
    # Convert to lowecase
    text=text.lower()
    
    # Replace contractions with their longer forms
    text=text.split()
    new_text=[]
    for word in text:
        if word in contractions:
            new_text.append(contractions[word])
        else:
            new_text.append(word)
    
    text=" ".join(new_text)
    
    # Format words and remove unwanted characters
    
    text = re.sub(r'https?:\/\/.[\r\n]', '', text, flags=re.MULTILINE)
    text = re.sub(r'\<a href', ' ', text)
    text = re.sub(r'&amp;', '', text) 
    text = re.sub(r'[_"\-;%()|+&=*%.,!?:<>#$@\[\]/]', ' ', text)
    text = re.sub(r'<br />', ' ', text)
    text = re.sub(r'\'', ' ', text)
    
    # Optionally, remove stop words
    if remove_stopwords:
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)

    return text

def predict():
  if request.method == 'POST':
      message = request.form['message']
      clean_data=clean_text(message)
      print(clean_data)
      my_prediction = sentiment.predict(clean_data)
      print(my_predictions)
  return render_template('result.html',prediction = my_prediction)

if __name__ == '__main__':
  app.run(debug = True)
  predict()