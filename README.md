Kubernetes
----------

Kubernetes is an open source implementation of container cluster management.


Usage
=====

This bundle can be used to deploy kubernetes onto any cloud it can be used 
directly in the gui or via the deployer cli::

 juju-deployer -vWSdc bundle.yaml

You'll need the kubernetes command line client to utlize the created cluster.

https://github.com/GoogleCloudPlatform/kubernetes/releases

Grab the tarball and from the extracted release you can just directly use the 
cli binary at ./kubernetes/platforms/linux/amd64/kubecfg

You'll need the address of the kubernetes master as environment variable:

   juju status kubernetes-master/0

Grab the public-address there and export it as KUBERNETES_MASTER environment
variable:
  
   export KUBERNETES_MASTER="x.y.z.d"

And now you can run through the kubernetes examples per normal.

   $ kubecfg list minions

You can add capacity by adding more minions

   $ juju add-unit kubernetes

Caveat
======

Kubernetes currently has several platform specific functionality. For example
load balancers and persistence volumes only work with the google compute 
provier. 

The juju integration uses the kubernetes null provider. This means external
load balancers and storage can't be directly driven through kubernetes config
files.




 





