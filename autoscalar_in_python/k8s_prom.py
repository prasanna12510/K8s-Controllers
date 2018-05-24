from prometheus_client import start_http_server, Summary, Histogram
import random
import time

#REQUEST_TIME = Summary('request_processing_seconds','Time spent processing request')
#s = Summary('request_latency_seconds', 'Description of summary')
h = Histogram('request_latency_seconds','Description of histogram')
h.observe(4.7)
#s.observe(4.7)
def process_request(t):
	"""A dummy function that takes some time."""
	time.sleep(t)

if __name__=='__main__':
	start_http_server(8800)

	while True:
		process_request(random.random())

