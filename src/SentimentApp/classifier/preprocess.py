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
        self.model = joblib.load(os.path.join(settings.BASE_DIR, "models/SVM_model_v2.joblib"))
        self.vectorizer = joblib.load(os.path.join(settings.BASE_DIR, "models/vectorizer.joblib"))

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

        # Regex pattern to match:
        # 1. URLs starting with 'http' or 'https'
        # 2. Characters that aren't word characters, whitespace, '@', or '#'
        # 3. Mentions (e.g., '@username') and hashtags (e.g., '#topic')
        # 4. Time patterns (e.g., '12:34')
        # 5. Numbers not followed by a letter
        # 6. Underscores
        pattern = re.compile(r'(http|https)://[^\s]+|[^\w\s@#]|(@\w+|#\w+)|\d+:\d+|\d+(?![a-zA-Z])|_')
        cleaned_text = pattern.sub(' ', text)
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
        stop_words = stopwords.words('English')
        stop_words.remove("not")
        stop_words = set(stop_words)
        
        for word in words:
            if word not in stop_words:
                filtered_words.append(word)

        # Lemmatize the text for nouns
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = []
        for word in filtered_words:
            lemmatized_word = lemmatizer.lemmatize(word, pos='n')
            lemmatized_words.append(lemmatized_word) 

        # Lemmatize for verbs
        final_lemmatized_words = []
        for word in lemmatized_words:
            lemmatized_word = lemmatizer.lemmatize(word, pos='v')
            final_lemmatized_words.append(lemmatized_word)
        
        processed_text = ' '.join(final_lemmatized_words)
        return processed_text
