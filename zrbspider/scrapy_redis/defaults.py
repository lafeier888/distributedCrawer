import redis
import json


with open('/var/www/zrbspider/zrbspider/url.json','r') as f:

# For standalone use.
    url= json.load(f)
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'

# PIPELINE_KEY = '%(spider)s:items'
PIPELINE_KEY = url['urldomain']+':items'

REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'
# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}

# SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
# SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
# SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
#
# START_URLS_KEY = '%(name)s:start_urls'


SCHEDULER_QUEUE_KEY = url['urldomain']+':requests'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
SCHEDULER_DUPEFILTER_KEY = url['urldomain']+':dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

START_URLS_KEY = '%(name)s:start_urls'
START_URLS_AS_SET = False
