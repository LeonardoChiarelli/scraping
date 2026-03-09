import hashlib
import redis

class DistributedFrontier:
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)

    def add_url(self, url, priority=0):
        fp = hashlib.sha256(url.encode()).hexdigest()
        is_new = self.redis.sadd("frontier:seen", fp)
        
        if is_new:
            self.redis.zadd("frontier:queue", {url: priority})
            return True
        return False

    def get_next_url(self):
        url_data = self.redis.zpopmax("frontier:queue", 1)
        if url_data:
            return url_data[0][0].decode('utf-8')
        return None