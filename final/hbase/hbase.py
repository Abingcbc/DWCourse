import happybase

connection = happybase.Connection('localhost')

# connection.create_table("movie",{
#     "cf": dict()
# })

# connection.create_table("review", {
#     "cf": dict()
# })

movie_table = connection.table("movie")
review_table = connection.table("review")

movie_attr = {'name':'name', 'star_score':'star',
              'restrict_level':'restrict', 'buy_price':'buy',
              'actors':'actors','directors':'directors',
              'writers':'writers','producers':'producers',
              'format':'format','language':'lan',
              'number_of_tapes':'tapes','asin':'asin',
              'year':'year','region':'region','number_of_discs':'discs',
              'studio':'studio','dvd_release_date':'ddate',
              'imdb_score':'imdb','time_len':'len','rent_price':'rent',
              'genres':'genres','starring':'starring',
              'supporting_actors':'sactors','audio_languages':'alan',
              'purchase_rights':'rights','subtitles':'subtitles',
              'aspect_ratio':'ratio','vhs_release_date':'vdate',
              'dubbed':'dubbed'}

with movie_table.batch() as movie_batch:
    with open("../result.txt", 'r') as file:
        temp_map = {}
        for line in file:
            field = line.strip().split(':')[0].replace(' ', '_')
            if field == '':
                continue
            attr = line.strip().split(':')[1]
            if field == 'id' and len(temp_map.keys()) != 0:
                movie_batch.put()


