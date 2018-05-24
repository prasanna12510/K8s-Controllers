from prometheus_client.parser import text_string_to_metric_families
from pydash import at
import requests


metrics = requests.get("https://api.usa-cluster.cto.logi.com/metrics" , auth=('admin', 'HbpsXEiyoE0GHbQMk3ZcXoXHjWMRhEeM'),verify=False).content

for family in text_string_to_metric_families(metrics):
	for sample in family.samples:
		if sample[0] == 'apiserver_request_latencies_summary':
			#for key,value in sample[1].iteritems():
				#if (key=='quantile' and value=='0.99') and (key=='verb' and value=='GET'):
					#print key,value
					list = at(sample[1],'resource','scope','subresource','verb','quantile')
					print list		

