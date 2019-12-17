import happybase
import pandas as pd

columns = \
    ['id', 'name', 'star', 'restrict', 'buy', 'actors',
     'directors', 'writers', 'producers', 'format',
     'lan', 'tapes', 'asin', 'region', 'discs', 'studio',
     'year', 'month', 'day', 'week', 'imdb', 'len', 'rent', 'genres',
     'starring', 'sactors', 'alan', 'rights', 'subtitles',
     'ratio', 'dubbed', 'supporter']

def queryMovieByTime(timeObject):
    connection = happybase.Connection("localhost")
    movie_table = connection.table("movie")
    filterString = ''
    count = 0
    for key, value in timeObject.items():
        if count != 0:
            filterString += ' AND '
        count += 1
        filterString += "SingleColumnValueFilter ('cf', '" + key + "', =, 'binary:" + str(value) + "', true, false)"
    count = 0
    result = []
    print(filterString)
    for key, data in movie_table.scan(
            filter=filterString):
        count += 1
        temp = {'id': key.decode()}
        for k, v in data.items():
            t = v.decode()
            try:
                t = float(v.decode())
            except:
                pass
            temp[k.decode()[3:]] = t
        result.append(temp)
    print('get ' + str(count) + ' movies')
    html = pd.DataFrame(result, columns=columns)[0:100].to_html()
    return html, count

if __name__ == '__main__':
    queryMovieByTime({'year': 2000, 'month': 7})

