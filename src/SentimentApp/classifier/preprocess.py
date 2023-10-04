from django.conf import settings
import joblib
import os
import warnings

# Regex
import re 

# NLTK
import nltk #for text preprocessing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings("ignore")
class MLConfig():
    def __init__(self):
        self.model = joblib.load(os.path.join(settings.BASE_DIR, "models/SVM_model_ver_1.joblib"))
        self.vectorizer = joblib.load(os.path.join(settings.BASE_DIR, "models/tfidf_vectorizer_ver_1.joblib"))

    def clean_text(self, text):
        """
        Removes @, #, and punctuation marks from the text.

        Parameters:
            text (str): tokenized tweet.
        Returns:
            str: The cleaned tweet text.
        """
        # Convert text to lowercase
        text = text.lower()

        # Replace @, #, links and non-word characters with a space
        pattern = re.compile(r'(http|https)://[^\s]+|[^\w\s@#]|[@#]|\d+:\d+|\d+(?![a-zA-Z])|_')
        cleaned_text = pattern.sub(' ', text)
        

        # Remove extra spaces
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text

    def preprocess_text(self, text):
        """
        Preprocesses the text.

        Parameters:
            text (str): tokenized tweet.
        Returns:
            str: The cleaned tweet text.
        """
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize the text
        words = word_tokenize(cleaned_text)
        filtered_words = []
        
        # Remove English Stop Words
        stop_words = set(stopwords.words('English'))

        for word in words:
            if word not in stop_words:
                filtered_words.append(word)
        # print("Filtered: ", filtered_words)
        
        # Lemmatize the text for nouns
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = []
        for word in filtered_words:
            lemmatized_word = lemmatizer.lemmatize(word, pos='n')
            lemmatized_words.append(lemmatized_word) 
        # print("Lemmatized words:", lemmatized_words)

        # Lemmatize for verbs
        final_lemmatized_words = []
        for word in lemmatized_words:
            lemmatized_word = lemmatizer.lemmatize(word, pos='v')
            final_lemmatized_words.append(lemmatized_word)
        
        processed_text = ' '.join(final_lemmatized_words)
        return processed_text
