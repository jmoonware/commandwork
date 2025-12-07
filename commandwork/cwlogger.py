
import logging
import logging.handlers

def StartDataLogging(log_file='log_cw.txt',level=logging.DEBUG,thing=1,log_queue=None):
	logger = logging.getLogger(__name__)
#	logFormatString='\t'.join(['%(asctime)s.%(msecs)03d','%(levelname)s','%(message)s'])
	logFormatString='\t'.join(['%(asctime)s','%(levelname)s','%(message)s'])
#	datefmt='%Y-%m-%dT%H:%M:%S'
	maxbytes=10000000
	handlers = []
	if log_queue!=None:
		lqh = logging.handlers.QueueHandler(log_queue)
		handlers.append(lqh)
		logFormatString='\t'.join(['%(process)s','%(message)s'])
	else:
		sh=logging.StreamHandler()
		handlers.append(sh)
		rfh=logging.handlers.RotatingFileHandler(filename=log_file,maxBytes=maxbytes,backupCount=10)
		handlers.append(rfh)
#	logging.Formatter(fmt=logFormatString, datefmt=datefmt)
	logging.basicConfig(format=logFormatString,handlers=handlers,level=level)
	logging.captureWarnings(True)
	logger.critical("Logging Started, level={0}".format(level))
	return logger, handlers
