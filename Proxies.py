import redis
import random

class RandomProxies():
    def __init__(self):
        self.host='192.168.0.102'
        self.port=6379
        self.db=redis.StrictRedis(host=self.host,port=self.port)

    def get_proxies(self):
        redis_proxies=self.db.zrangebyscore('proxies',90,100)
        proxy=random.choice(redis_proxies)
        proxy=bytes.decode(proxy)
        proxies={
            'http':'http://'+proxy,
            'https':'https://'+proxy,
        }
        return proxies
