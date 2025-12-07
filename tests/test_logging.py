import sys
sys.path.append("..")

from commandwork.worker import Worker
from commandwork.cwlogger import *
import multiprocessing as mp
import time
import os

num_workers = 5

# Starting logging here causes log entries to be dropped (either in 
# pytest or running in the Python interpreter)
#
# However, starting in the test function means pytest uses
# whatever format is in pytest.ini (and won't log to file as 
# specified in StartDataLogging), although the file is created.
#
# Apparently, the listener will log to file using the correct format
# specified in StartDataLogging for each process,  but will
# not use the pytest OR the root StartDataLogger basic format!
#
# Starting logging in the test_logging function and running in the Python
# interpreter produces the desired log behavior, though
# 
# logger, handlers = StartDataLogging(log_file="oneproc_log.txt")

def work_proc(worker_id,logq=None):
	wk = Worker(settings={'log_queue':logq,'blocking':False})
	wk.Run()
	time.sleep(1)

def test_logging():
	logger, handlers = StartDataLogging(log_file="oneproc_log.txt")
	
	print("*** Start sp test")
	wk1 = Worker()
	wk2 = Worker()
	wk1.Run()
	wk2.Run()
	time.sleep(1)
	wk1.Stop()
	wk2.Stop()
	
	print("*** Start mp test")
	mp.set_start_method("spawn")
	logq = mp.Queue()
	listener = logging.handlers.QueueListener(logq, *handlers)
	procs = []
	listener.start()
	for i in range(num_workers):
		p = mp.Process(target=work_proc,args=(str(i),logq))
		p.start()
		procs.append(p)
	for p in procs:
		p.join()
	listener.stop()

if __name__=="__main__":
	test_logging()
