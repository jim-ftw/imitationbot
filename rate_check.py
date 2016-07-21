import logging
import sys
import time

logger = logging.getLogger(__name__)

def rate_check(headers):
	logger.debug('rate limit check')
	rate_limit_remaining = headers['X-Ratelimit-Remaining']
	rate_limit_reset = int(headers['X-Ratelimit-Reset'])
	now = int(time.time())
	if int(rate_limit_remaining) < 3:
		if int(rate_limit_reset) < 100:
			sleep_time = rate_limit_reset
		else:
			sleep_time = rate_limit_reset - now
		logger.info('sleeping for: ' + str(sleep_time))
		time.sleep(sleep_time)