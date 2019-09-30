from redis import StrictRedis

def init(spider_name, domain, file_path, host='localhost', port=6379, db=0, password=''):
    redis = StrictRedis(host=host, port=port, db=db, password=password)
    key = spider_name + ':start_urls'
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i >= 10:
                break
            redis.lpush(key, domain+line)

init('amazon', 'https://www.amazon.com/dp/', 
'/Users/cbc/Project/DWCourse/homework1/data/movies_id.txt',password='friday')