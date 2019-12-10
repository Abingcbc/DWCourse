import happybase
import pandas as pd

connection = happybase.Connection("localhost")
print('connect hbase successfully\n')

# connection.create_table("movie", {"cf": dict()})
# connection.create_table("review", {"cf": dict()})
# print('create table successfully\n')

movie_table = connection.table("movie")
review_table = connection.table("review")

movie_attr = {
    "name": "name",
    "star_score": "star",
    "restrict_level": "restrict",
    "buy_price": "buy",
    "actors": "actors",
    "directors": "directors",
    "writers": "writers",
    "producers": "producers",
    "format": "format",
    "language": "lan",
    "number_of_tapes": "tapes",
    "asin": "asin",
    "region": "region",
    "number_of_discs": "discs",
    "studio": "studio",
    "year": "year",
    "month": "month",
    "day": "day",
    "imdb_score": "imdb",
    "time_len": "len",
    "rent_price": "rent",
    "genres": "genres",
    "starring": "starring",
    "supporting_actors": "sactors",
    "audio_languages": "alan",
    "purchase_rights": "rights",
    "subtitles": "subtitles",
    "aspect_ratio": "ratio",
    "dubbed": "dubbed",
    "supporter":"supporter"
}

df = pd.read_csv('../../movies.csv', dtype=str)
count = 0
for index, row in df.iterrows():
    temp_map = {}
    for attr in movie_attr.keys():
        if pd.notna(row[attr]):
            temp_map['cf:'+movie_attr[attr]] = row[attr]
    movie_table.put(row['id'], temp_map)
    count += 1
    if count % 10000 == 0:
        print('----' + str(count) + '----')
print(count)

with open('../not_insert.txt','w') as file:
    for index, row in df.iterrows():
        if len(movie_table.row(row['id'])) == 0:
            file.write(row['id']+'\n')
        if index % 10000 == 0:
            print(index)