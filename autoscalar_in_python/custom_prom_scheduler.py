from kubernetes import client, config, watch
from prometheus_client import Summary,start_http_server
import time 
import random

config.load_kube_config()
v1=client.CoreV1Api()

scheduler_name = "my-scheduler"

def get_request_time(hostname):
    s = Summary('request_latency_seconds', 'Description of summary')
    request_time = s.observe(4.7)
    print "summary of request latency: "+ request_time
    return request_time


def best_request_time(nodes):
    if not nodes:
        return []
    node_times = [get_request_time(hostname) for hostname in nodes]
    best_node = nodes[node_times.index(min(node_times))]
    print "Best node: " + best_node
    return best_node


def nodes_available():
    ready_nodes = []
    for n in v1.list_node().items:
            for status in n.status.conditions:
                if status.status == "True" and status.type == "Ready":
                    ready_nodes.append(n.metadata.name)
    return ready_nodes


def scheduler(name, node, namespace="default"):
    body=client.V1Binding()
    target=client.V1ObjectReference()
    target.kind="Node"
    target.apiVersion="v1"
    target.name= node
    meta=client.V1ObjectMeta()
    meta.name=name
    body.target=target
    body.metadata=meta
    return v1.create_namespaced_binding(namespace, body)


def main():
    print "In Main"
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, "default"):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
            try:
                print "Scheduling " + event['object'].metadata.name
                res = scheduler(event['object'].metadata.name, best_request_time(nodes_available()))
            except client.rest.ApiException as e:
                print json.loads(e.body)['message']


if __name__ == '__main__':
	main() 