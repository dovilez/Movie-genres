import pickle
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
import scraping.scraping as scraping

def main():
    # search_words = ['action', 'comedy', 'sci-fi', 'horror', 'romance', 'thriller', 'drama', 'mystery', 'crime',
    #                'animation', 'adventure', 'fantasy', 'superhero']
    # df = scraping.collect_keywords(search_words, 100)
    # df.to_csv("imdb.csv")

    df = pd.read_csv("imdb.csv").dropna()
    df = prepare_dataframe(df)
    train_model(df)
    print(df)


def prepare_dataframe(df):
    """
    Function to prepare the dataframe
    :param df: DataFrame to prepare
    :return: clean DataFrame for training
    """
    df = df.drop_duplicates()
    df["genre"] = df["genre"].apply(eval)
    df["clean_plot"] = df["plot"].apply(lambda x: clean_text(x))
    df["clean_plot"] = df["clean_plot"].apply(lambda x: remove_stopwords(x))
    return df


def clean_text(text):
    """
    Function for text cleaning
    :param text: text to clean
    :return: cleaned text
    """
    text = re.sub("'", "", text)
    text = re.sub("[^a-zA-Z]", " ", text)
    text = " ".join(text.split())
    text = text.lower()
    return text


def remove_stopwords(text):
    """
    Function to remove stopwords
    :param text: text to clean
    :return: text with removed stopwords
    """
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return " ".join(no_stopword_text)


def train_model(df):
    """
    Function to train the model
    :param df: DataFrame for training
    """
    multilabel_binarizer = MultiLabelBinarizer()
    multilabel_binarizer.fit(df["genre"])
    pickle.dump(multilabel_binarizer, open("model/binarizer.pkl", "wb"))

    y = multilabel_binarizer.transform(df["genre"])

    xtrain, xval, ytrain, yval = train_test_split(
        df["clean_plot"], y, test_size=0.2, random_state=9
    )

    # create TF-IDF features
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000)
    xtrain_tfidf = tfidf_vectorizer.fit_transform(xtrain)
    pickle.dump(tfidf_vectorizer, open("model/vectorizer.pkl", "wb"))
    #xval_tfidf = tfidf_vectorizer.transform(xval)

    lr = LogisticRegression()
    clf = OneVsRestClassifier(lr)

    clf.fit(xtrain_tfidf, ytrain)
    pickle.dump(clf, open("model/classifier.pkl", "wb"))


if __name__ == "__main__":
    main()