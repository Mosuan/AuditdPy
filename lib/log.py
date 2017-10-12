#-*- coding:utf-8 -*-

import os
import time

class Log(object):

	def __init__(self):
		self.error_log = '/tmp/auditd_py_error.log'

	def _time(self):
		return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

	def _ip(self):
		return os.popen("ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6 | awk '{print $2}' | tr -d 'addr:'").read()

	def _file(self, filename, msg=''):
		'''
		filename add
		'''
		if not os.path.exists(filename):
			objs = open(filename,"w+")
			objs.close()
		file_obj = open(filename, "a")
		content = file_obj.write(msg)
		file_obj.close()

	def debug(self, msg):
		time = self._time()
		ip = str(self._ip()).replace("\n"," ")
		error = str("time=%s msg=%s" % (time, str(msg)))
		msg = "{\"level\":\"debug\", \"error\": \"%s\", \"time\": \"%s\", \"ip\": \"%s\"}" % (msg, time, ip)
		self._file(self.error_log, error+"\n")
		if not 'Redis' in msg:
			from RedisAdd import Redis
			Redis().push_msg(str(msg))

if __name__ == '__main__':
	Log().debug("debug log test!")