# "C:\ProgramData\Anaconda3\condabin\conda.bat"
from bs4 import BeautifulSoup
import requests
import pandas as pd

main_link = r"https://worldathletics.org/records/all-time-toplists/sprints/100-metres/outdoor/women/senior"
relevant_cols = [
    "Rank", "Mark", "WIND", "Competitor", "DOB", "Nat", "Venue", "Date", "ResultScore"
]
df_dict = {
    "AllTime":
        {"100m":
             {"Women": pd.DataFrame(
                 columns=relevant_cols
             )
             }
        }
}

idx = 1
curr_link = main_link
df_loc = df_dict["AllTime"]["100m"]["Women"]

while True:

    page = requests.get(curr_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_tables = soup.find_all("table")

    if len(all_tables) == 0:
        break

    table = all_tables[0]

    for row in table.tbody.find_all('tr'):
        cols = row.find_all("td")
        row_dict = {}
        for el in cols:
            row_dict.update({el.attrs["data-th"]: el.text.strip()})

        df_loc = df_loc.append(pd.Series(row_dict)[relevant_cols], ignore_index=True)


    curr_link = f"{main_link}?page={idx}"
    idx += 1

print("chek")

