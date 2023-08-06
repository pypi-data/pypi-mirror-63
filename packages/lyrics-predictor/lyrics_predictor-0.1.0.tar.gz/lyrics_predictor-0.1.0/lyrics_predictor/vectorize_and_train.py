"""This file contains a function to train a model on the lyrics."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def clean_vectorize_train_naive_bayes(csv1, csv2):
    """
    This function clean and vectorize the lyrics by Tfidf and finally train
    a naive bayes model and predict which artist the given lyrics belongs.
    """
    df1 = pd.read_csv(f"{csv1} Lyrics.csv", index_col=0)
    df2 = pd.read_csv(f"{csv2} Lyrics.csv", index_col=0)
    df = pd.concat([df1, df2])
    df.dropna(inplace=True)
    df.reset_index(inplace=True)

    tv_Tf = TfidfVectorizer(ngram_range=(1, 1), lowercase=True)
    vector_tfidf = tv_Tf.fit_transform(df["lyrics"])
    df_all = pd.DataFrame(vector_tfidf.todense())

    X_train = df_all
    y_train = df["Artist"]

    m_t = MultinomialNB(alpha=0.001)
    m_t.fit(X_train, y_train)
    return m_t, tv_Tf

def predcit_func(lyrics, m_t, tv_Tf):
    X_test = tv_Tf.transform([lyrics]).todense()
    prediction = m_t.predict(X_test)
    return print(f"This song belongs to {prediction}")
