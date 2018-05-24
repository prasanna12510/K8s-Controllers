#!/bin/sh

Out=$(curl -k -u admin:HbpsXEiyoE0GHbQMk3ZcXoXHjWMRhEeM  https://api.usa-cluster.cto.logi.com/apis/custom.metrics.k8s.io/v1beta1/namespaces/default/pods/*/http_requests_count | jq .'items')

for row in $(echo "${Out}" | jq -r '.[] | @base64'); do
    _jq() {
     echo ${row} | base64 --decode | jq -r ${1}
    }

   echo  $(_jq '.metricName') + " " + $(_jq '.value')
done