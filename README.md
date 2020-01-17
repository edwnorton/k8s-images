# k8s-images
## 在主服务器上调度pod
`kubectl taint nodes --all node-role.kubernetes.io/master-`

## 镜像无法下载，修改镜像源
`sed -i "s/quay.io/quay.azk8s.cn/g" *.yaml`

## secret "rook-ceph-crash-collector-keyring" not found
删除dataDirHostPath: /var/lib/rook，重新创建

## 修改默认storageclass
`kubectl patch storageclass <your-class-name> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'`
