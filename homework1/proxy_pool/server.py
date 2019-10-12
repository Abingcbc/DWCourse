from flask import Flask
import redis
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from flask import g
import random

app = Flask(__name__)

@app.route('/get')
def get():
    db = redis.Redis(connection_pool=g.cp)
    length = db.llen('proxies')
    proxy = db.lindex('proxies', random.randint(0, length))
    return {'proxy': db.get()}

@app.route('/delete/<proxy>')
def delete(proxy):
    db = redis.Redis(connection_pool=g.cp)
    db.lrem('proxies',proxy)

@app.route('/valid')
def valid():
    db = redis.Redis(connection_pool=g.cp)
    if db.llen('proxies') == 0:
        return {'valid': False}
    else:
        return {'valid': True}

def get_proxies():
    url = ''
    response = requests.get(url)
    if response.status_code == 200:
        db = redis.Redis(connection_pool=g.cp)
        msg = eval(response.text)['msg']
        for p in msg:
            db.rpush('proxies', p['ip']+':'+p['port'])

if __name__ == '__main__':
    ctx = app.app_context()
    ctx.push()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=1, password='friday')
    g.cp = pool
    app.run()