
import logging
import logging.handlers

def StartDataLogging(log_file='log_cw.txt',level=logging.DEBUG):
	logger = logging.getLogger(__name__)
	logFormatString='\t'.join(['%(asctime)s','%(levelname)s','%(message)s'])
	# unique-ish log name every startover
	maxbytes=10000000
	rfh=logging.handlers.RotatingFileHandler(filename=log_file,maxBytes=maxbytes,backupCount=10)
	sh=logging.StreamHandler()
	logging.basicConfig(format=logFormatString,handlers=[sh,rfh],level=level)
	logging.captureWarnings(True)
	logger.critical("Logging Started, level={0}".format(level))
	return logger
