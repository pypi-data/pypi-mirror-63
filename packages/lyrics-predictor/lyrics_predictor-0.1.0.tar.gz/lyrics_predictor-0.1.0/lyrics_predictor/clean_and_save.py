
"""Clean and save as CSV"""
import re
import pandas as pd


def clean_and_save_as_csv(lyrics, artist):
    """
    clean and save the lyrics as csv file.

    lyrics: all the lyrics in a list foramt

    returns a dataframe with cleaned lyrics
    and save it as a csv file with all the lyrics of the artist
    """

    clean_list = []
    for song in lyrics:
        clean_lyric = str(song)
        clean_lyric = re.sub(r"<.{2,30}>|\n", " ", clean_lyric)
        clean_lyric = re.sub(r"[]]|[[]|\\", "", clean_lyric)
        clean_list.append(clean_lyric)

    df = pd.DataFrame()
    df["lyrics"] = clean_list
    df["Artist"] = artist
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df = df[ ~df["lyrics"].str.contains("instrumental")]
    df = df[ ~df["lyrics"].str.contains("Unfortunately, we are not authorized to show these lyrics")]
    df = df[ ~df["lyrics"].str.contains("Instrumental")]
    print(f"{artist} lyrics has been saved in the folder")
    return df.to_csv(f"{artist} Lyrics.csv")
