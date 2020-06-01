#!/bin/bash
USER=root
PLANE_IPS="172.16.13.60 172.16.13.61"
for host in ${PLANE_IPS}; do
scp /etc/kubernetes/pki/ca.crt "${USER}"@$host:/etc/kubernetes/pki/ca.crt
scp /etc/kubernetes/pki/ca.key "${USER}"@$host:/etc/kubernetes/pki/ca.key
scp /etc/kubernetes/pki/sa.key "${USER}"@$host:/etc/kubernetes/pki/sa.key
scp /etc/kubernetes/pki/sa.pub "${USER}"@$host:/etc/kubernetes/pki/sa.pub
scp /etc/kubernetes/pki/front-proxy-ca.crt "${USER}"@$host:/etc/kubernetes/pki/front-proxy-ca.crt
scp /etc/kubernetes/pki/front-proxy-ca.key "${USER}"@$host:/etc/kubernetes/pki/front-proxy-ca.key
scp /etc/kubernetes/pki/etcd/ca.crt "${USER}"@$host:/etc/kubernetes/pki/etcd/ca.crt
scp /etc/kubernetes/pki/etcd/ca.key "${USER}"@$host:/etc/kubernetes/pki/etcd/ca.key
scp /etc/kubernetes/admin.conf "${USER}"@$host:/etc/kubernetes/admin.conf
done
