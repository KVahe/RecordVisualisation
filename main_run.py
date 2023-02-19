# "C:\ProgramData\Anaconda3\condabin\conda.bat"
from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask import json

from record_db import *
# import postprocessing as pp

warnings.simplefilter(action='ignore', category=FutureWarning)
init_link = r"https://worldathletics.org/records/all-time-toplists/TYPE/SUBTYPE/outdoor/GENDER/senior"
relevant_cols = [
    "Rank", "Mark", "WIND", "Competitor", "DOB", "Nat", "Venue", "Date", "ResultScore"
]
df_dict = {
    "AllTime": {}
}

genders = ["Men", "Women"]
type_list = [
    # ("sprints", "100-metres", []),
    # ("sprints", "200-metres", []),
    # ("middle-long", "1000-metres", []),
    # ("middle-long", "5000-metres", []),
    # ("middle-long", "10000-metres", []),
    # ("road-running","marathon", []),
    # ("jumps", "high-jump", []),
    # ("jumps", "pole-vault", []),
    # ("jumps", "long-jump", []),
    # ("jumps", "triple-jump", []),
    # ("throws", "shot-put", ["WIND"]),
    # ("throws", "discus-throw", ["WIND"]),
    # ("throws", "hammer-throw", ["WIND"]),
    ("throws", "javelin-throw", ["WIND"]),

]

start_time = time.time()
for type_v in type_list:
    df_dict["AllTime"][f"{type_v[0]}_{type_v[1]}"] = {}
    fin_cols = [i for i in relevant_cols if i not in type_v[2]]
    for gender in genders:
        print(f"Current Run: {type_v[0]}_{type_v[1]} -- {gender}")
        main_link = (
            init_link
            .replace("GENDER", gender.lower())
            .replace("SUBTYPE", type_v[1])
            .replace("TYPE", type_v[0])
        )
        df_dict["AllTime"][f"{type_v[0]}_{type_v[1]}"][gender] = pd.DataFrame(
            columns=fin_cols
        )
        df_loc = df_dict["AllTime"][f"{type_v[0]}_{type_v[1]}"][gender]
        idx = 1
        curr_link = main_link

        while True:

            page = requests.get(curr_link)
            soup = BeautifulSoup(page.content, 'html.parser')
            all_tables = soup.find_all("table")

            if len(all_tables) == 0 or idx > 100:
                print(f"Time Spent: {time.time() - start_time}")
                break

            table = all_tables[0]

            for row in table.tbody.find_all('tr'):
                cols = row.find_all("td")
                row_dict = {}
                for el in cols:
                    row_dict.update({el.attrs["data-th"]: el.text.strip()})

                df_loc = df_loc.append(pd.Series(row_dict)[fin_cols], ignore_index=True)


            curr_link = f"{main_link}?page={idx}"
            idx += 1

        df_dict["AllTime"][f"{type_v[0]}_{type_v[1]}"][gender] = df_loc


db_driver = "postgresql+psycopg2"
db_user = "postgres"
db_pass = "swordfish"
db_host = "localhost"
db_port = "5432"
db_name = "postgres"
args = ""

db_engine = create_engine(
    f"{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}{args}",
    pool_recycle=1200,
    pool_use_lifo=True,
    pool_pre_ping=True,
    pool_size=20,
    json_serializer=json.dumps,
    json_deserializer=json.loads,
)

input_json = jsonize_data(df_dict)
output_json = "{}"
session = Session(bind=db_engine)
m_run = Run(created_on=datetime.now())
session.add(m_run)
session.flush()
run_id = m_run.id
input = RecordsInputJson(payload=input_json, run_id=run_id)
output = RecordsOutputJson(payload=output_json)
session.add(input)
session.add(output)
session.flush()
session.close()

type_dict = {
    "gender": genders,
    "sport": type_list,
    "record": "AllTime"
}
save_structured_data(session, type_dict, input_json)


print("")

