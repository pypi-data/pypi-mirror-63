"""This file gets the urls of the first 2 pages and scrape the lyrics."""
from bs4 import BeautifulSoup
from lyrics_predictor.clean_and_save import clean_and_save_as_csv
import requests
import os.path

def get_urls(artist):
    """
    Gets the urls.

    This function takes an artits name and returns the urls of the first two pages
    """
    artist_name = artist.lower().strip().split(' ')
    artist_name = '-'.join(artist_name)

    all_pages = []
    for i in range(1, 3):
        page = f"https://www.metrolyrics.com/{artist_name}-alpage-{i}.html"
        all_pages.append(page)
    return all_pages, artist

def lyrics_scraper(urls, short = False):
    """
    Scrapes every lyrics in the artist page.

    ursl: urls of the first two pages of the artist with links of the lyrics

    returns a list of the scraped lyrics using BeautifulSoup
    """
    all_lyrics = []
    for u in urls:
        page = requests.get(u)
        b_all = BeautifulSoup(page.text, "html.parser")
        links = b_all.find_all(attrs={"class":"songs-table compact"})[0].find_all('a')
        if short:   #for the test file to scrape only 2 lyrics
            links = links[:2]
        for link in links:
            lyrics_url = link.get("href")
            lyric_url = requests.get(lyrics_url)
            lyric_parser = BeautifulSoup(lyric_url.text, "html.parser")
            lyrics = lyric_parser.find_all(attrs={"id":
                                           "lyrics-body-text"})[0].find_all("p")
            all_lyrics.append(lyrics)

    return all_lyrics

def get_urls_scrape_save_as_csv(ARTIST):
    """
    Get urls, scrapes and save as csv.

    If the csv file already exist this function will pass.
    ARTIST: name of the artist as string

    returns dataframe and save it as a csv file with all lyrics and the name of the artist
    """
    if os.path.isfile(f'{ARTIST} Lyrics.csv'):
        print(f"The {ARTIST} file already exist. The model will be train on that file")
    else:
        urls, artist = get_urls(ARTIST)
        lyrics = lyrics_scraper(urls)
        clean_and_save_as_csv(lyrics, artist)
