
import sys

sys.path.append("..")
sys.path.append("../commandwork")

from commandwork.worker import *
from commandwork.controller import *
from commandwork.exception_handler import *
from commandwork.cwlogger import *

import time

class wk(Worker):
	def Init(self):
		self.count=0		
	def Enter(self):
		self.logger.debug("Hi there")
	def Execute(self):
		self.logger.debug("{0}".format(self.count))
		self.count+=1
		raise ValueError("Uh oh! I threw an exception")
	def Exit(self):
		self.logger.debug("asdasd")
		print("I'm done")

def test_init(caplog):
	caplog.set_level(logging.NOTSET,logger='worker')
	StartDataLogging(log_file='log_testcontroller.txt')
	wk1 = wk(settings={'loop_count':3,'loop_interval':0.2})
	wk2 = Worker() 
	cnt = Controller()
#	breakpoint()
	cnt.RunRecipe([wk1,wk2],once=True)
	time.sleep(2)
	assert cnt.Status() == True
	assert wk1.exception_count == 1
	cnt.Stop()
	logging.shutdown()
