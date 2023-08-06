""" This is the main py file to run the program.

It accepts three outputs:
 1. Name of the first artist
 2. Name of the second artist
 3. The lyrics that the user wants to predict

 If the csv file of the artist's lyrics doesnt exist the program scrape it and
 save it as csv file and train a naive bayes model to predict the artitst of
 the given lyrics.
 """
import os.path
from lyrics_predictor.vectorize_and_train import clean_vectorize_train_naive_bayes
from lyrics_predictor.vectorize_and_train import predcit_func
from lyrics_predictor.get_urls_and_scrape import get_urls, lyrics_scraper
from lyrics_predictor.get_urls_and_scrape import get_urls_scrape_save_as_csv
from lyrics_predictor.clean_and_save import clean_and_save_as_csv


if __name__ == '__main__':
    print("Please enter the name of the first artist:\n")
    ARTIST_1 = input()
    print("Please enter the name of the second artist:\n")
    ARTIST_2 = input()
    get_urls_scrape_save_as_csv(ARTIST_1)
    get_urls_scrape_save_as_csv(ARTIST_2)
    m_t, tv_Tf = clean_vectorize_train_naive_bayes(ARTIST_1, ARTIST_2)

    print("\nWrite a song that you want to predict or write END to finish:\n")
    LYRICS = input()
    while LYRICS != "END":
        predcit_func(LYRICS, m_t, tv_Tf)
        print("Write another song that you want to predict or write END to finish:\n")
        LYRICS = input()
    if LYRICS == "END":
        print("Thank you and see you soon!")
