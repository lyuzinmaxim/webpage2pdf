import pandas as pd
import requests
from weasyprint import HTML
from pathlib import Path
from tqdm import tqdm
import time
from datetime import datetime
import numpy as np


HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x32)"
    "AppleWebKit/537.11 (KHTML, like Gecko) "
    "Chrome/117.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en,de-DE;q=0.9,de;q=0.8,en-US;q=0.7,ru;q=0.6",
    "Connection": "keep-alive",
}


def load_html(url_link, header=HEADER, retries=5, timeout=5):
    for _ in range(retries):
        try:
            response = requests.get(url=url_link, headers=header, timeout=timeout)
            return response.content
        except requests.RequestException as e:
            print(f"Error while fetching {url_link}: {e}, trying one more time...")
            time.sleep(timeout)
    print(f"Failed to load HTML from {url_link} after {retries} attempts.")
    return None


def convert_html_to_pdf(html_string, output_filename):
    html = HTML(string=html_string)
    html.write_pdf(output_filename)


def get_df(path_to_file):
    return pd.read_excel(path_to_file)


def check_url(url_link):
    if not url_link.startswith("http"):
        url_link = "http://" + url_link
    return url_link


def get_time(dataframe, link):
    date = dataframe.loc[dataframe["Web-link"] == link, "Date"].values[0]
    if isinstance(date, datetime):
        date = date.strftime("%Y-%m-%d_")
    elif isinstance(date, np.datetime64):
        date = str(date.astype("datetime64[D]"))
    else:
        date = str(date)
    return date


if __name__ == "__main__":
    output_directory = Path("pdf_files")
    output_directory.mkdir(parents=True, exist_ok=True)

    df = get_df("ClimateChange_Russia_CMB.xlsx")
    links = df["Web-link"].dropna().to_list()

    for link in tqdm(links):
        date_info = get_time(df, link)
        filename = date_info + "_" + "_".join(link.split("/")[-2:]) + ".pdf"
        html_string = load_html(check_url(link))
        if html_string:
            if ".pdf" in link:
                with open(output_directory / filename, "wb") as f:
                    f.write(html_string)
            else:
                convert_html_to_pdf(
                    html_string.decode("utf-8"), str(output_directory / filename)
                )
        else:
            print(f"Skipping, page {check_url(link)} could not be reached ")
