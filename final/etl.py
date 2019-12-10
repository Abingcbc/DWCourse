import pandas as pd

origin_attr = ['id', 'name', 'star_score', 'restrict_level', 'buy_price',
              'actors', 'directors', 'writers', 'producers',
              'format', 'language', 'number_of_tapes', 'asin',
              'year', 'region', 'number_of_discs', 'studio',
              'imdb_score', 'time_len', 'rent_price', 'genres', 'starring',
              'supporting_actors', 'audio_languages', 'purchase_rights', 'subtitles',
              'aspect_ratio', 'dubbed']
month_map = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6,
             'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}


df = []
count = 0
with open('results.txt', 'r') as file:
    tmp_map = {}
    for line in file:
        split_arr = line.strip().split(':')
        field = split_arr[0].strip().lower().replace(' ', '_')
        if field == '' or len(split_arr) == 1:
            continue
        attr = split_arr[1].strip().lower()
        if field == 'id':
            if tmp_map.get('id', None) is not None:
                df.append(tmp_map)
                count += 1
                if count % 10000 == 0:
                    print(count)
            tmp_map = {'id': attr}
        else:
            if field == 'director':
                field = 'directors'
            # There are some errors in `year` in some movies such as movie 6305167672,
            # so if there is `date`, it is better to override `year`.
            if field == 'year' and tmp_map.get('year', -1) == -1:
                tmp_map[field] = attr
            if field == 'vhs_release_date' or field == 'dvd_release_date':
                tmp_map['supporter'] = field[0:3]
                field = 'year'
                date_split = attr.split(',')
                attr = date_split[-1].strip()
                tmp_map['month'] = month_map[date_split[0].strip().split(' ')[0].strip()]
                tmp_map['day'] = date_split[0].strip().split(' ')[1].strip()
            if field in origin_attr:
                tmp_map[field] = attr
    df.append(tmp_map)
# df = pd.DataFrame(df, columns=movie_attr)
# df.to_csv('movies.csv')
