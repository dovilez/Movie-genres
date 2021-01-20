import requests
from bs4 import BeautifulSoup
import pandas as pd
import math


def collect_information(keyword: str, item_number: int) -> pd.DataFrame:
    """
    Scrape information about the movies of a given genre
    :param keyword: The movie genre to scrape
    :param item_number: The number of items to scrape
    :return: The dataframe with the information about scraped items
    """
    titles, years, ratings, genres, durations, IMDb_ratings, plots, pictures = (
        [] for i in range(8)
    )
    pages_number = math.ceil(item_number / 50)
    for page_no in range(0, pages_number):
        page = requests.get(
            f"https://www.imdb.com/search/title/?genres={keyword}&start={page_no*50+1}&explore=title_type,genres&ref_=adv_nxt",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        soup = BeautifulSoup(page.content, "html.parser")

        for item in soup.find_all("div", class_="lister-item"):
            header = item.find("h3", class_="lister-item-header")
            titles.append(header.find("a").text.replace("\n", ""))
            years.append(
                header.find("span", class_="lister-item-year").text.replace("\n", "")
            )
            genres.append(item.find("span", class_="genre").text.replace("\n", ","))

            duration = item.find("span", class_="runtime")
            if duration:
                durations.append(duration.text.replace("\n", ""))
            else:
                durations.append("")

            imdb_r = item.find("div", class_="ratings-imdb-rating")
            if imdb_r:
                IMDb_ratings.append(imdb_r.text.replace("\n", ""))
            else:
                IMDb_ratings.append("")

            rating = item.find("span", class_="certificate")
            if rating:
                ratings.append(rating.text.replace("\n", ""))
            else:
                ratings.append("")

            p = item.find_all("p", class_="text-muted")
            if p[1]:
                plots.append(p[1].text.replace("\n", ","))
            else:
                plots.append("")

            pictures.append(item.find("img", class_="loadlate")["src"])

    return pd.DataFrame(
        {
            "title": titles,
            "year": years,
            "duration": durations,
            "genre": genres,
            "rating": ratings,
            "plot": plots,
            "imdb": IMDb_ratings,
            "picture": pictures,
        }
    )


def process_data(df):
    """
    :param df: DataFrame to process
    :return: processed DataFrame
    """
    df = df.replace(regex={r"^,": "", r"^\(": "", r"\)$": ""})
    df["duration"] = df["duration"].replace(regex={r" min$": ""})
    df["year"] = df["year"].replace(regex={r"–.*$": ""})
    df["genre"] = df["genre"].replace(regex={r"\s+": ""})
    df["genre"] = df["genre"].str.split(",")
    return df


def collect_keywords(keywords, item_number) -> pd.DataFrame:
    """
    Scrape information from all genres and combine dataframes
    :param keywords: The list of movie genres to scrape
    :param item_number: The number of items to scrape
    :return: The dataframe with the information about scraped items from all genres
    """
    dataframes = []
    for keyword in keywords:
        frame = collect_information(keyword, item_number)
        dataframes.append(frame)

    df = pd.concat(dataframes).reset_index(drop=True)
    df = process_data(df)
    return df
