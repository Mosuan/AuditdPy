#-*- coding:utf-8 -*-

import time
import redis

from log import Log
from config import *

class Redis(object):

	def push_msg(self, msg):
		try:
			r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_pass)
			r.rpush(redis_key, msg)
			time.sleep(0.01)
		except Exception,e:
			Log().debug("RedisAdd.py push_msg error: %s" % (str(e)))


if __name__ == '__main__':
	obj = Redis()
	obj.push_msg('{"Mosuan":"unravel"}')
