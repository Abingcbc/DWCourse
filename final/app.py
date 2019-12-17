from flask import Flask
from flask import request
from hbase.v1.query import *

app = Flask(__name__, static_url_path="")

keyword2Query = {
    'year': queryMovieByTime
}

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route('/query')
def query():
    count = 0
    result = ''
    query_map = {}
    for key, value in request.args.items():
        print(str(key) + ': ' + str(value))
        query_map[key] = value
    result, count = keyword2Query['year'](query_map)
    return {
        'count': count,
        'result': result
    }


if __name__ == '__main__':
    app.run()
