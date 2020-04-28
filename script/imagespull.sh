#!/bin/bash
gcr_url=k8s.gcr.io
aliyun_url=registry.aliyuncs.com/google_containers

kube_version=v1.15.7
pause_version=3.1
etcd_version=3.3.10
coredns_version=1.3.1

images=(kube-apiserver:${kube_version}
kube-controller-manager:${kube_version}
kube-scheduler:${kube_version}
kube-proxy:${kube_version}
pause:${pause_version}
etcd:${etcd_version}
coredns:${coredns_version}
)

for imagename in ${images[@]} ; do
  docker pull $aliyun_url/$imagename
  docker tag $aliyun_url/$imagename $gcr_url/$imagename
  docker rmi $aliyun_url/$imagename
done
