Kubernetes
----------

Kubernetes is an open source implementation of container cluster management.

More info @ https://github.com/GoogleCloudPlatform/kubernetes

Juju is an opensource cloud orchestration and provisioning system.

More info @ https://juju.ubuntu.com

Usage
=====

You'll need the juju client as a pre-requisite, its available for windows, mac, and linux (@ https://juju.ubuntu.com/install/). For deploying the bundle here, i recommend the juju-quickstart tool
which works on mac ( brew install juju-quickstart ) or linux/ubuntu (apt-get install juju-quickstart).

This bundle can be used to deploy kubernetes onto any cloud it can be used
directly in the juju gui or via the juju-quickstart or deployer cli :

    juju quickstart bundle:~hazmat/kubernetes/kubernetes
    juju expose kubernetes-master


The quickstart package will present a curses ui to get you started on any
supported cloud platform. After that the bundle will launch 4 machines (etcd,
kubernetes-master, 2x minions w/ flannel).

Development Bundle: For charm developers / contributions
--------------------------------------------------------

    mkdir -p ~/charms/trusty
    git clone https://github.com/whitmo/kubernetes-charm.git ~/charms/trusty/kubernetes
    git clone https://github.com/whitmo/kubernetes-master-charm.git ~/charms/trusty/kubernetes-master

    juju quickstart develop.yaml
    juju expose kubernetes-master


Kubernetes Client Setup
---------------------------

You'll need the kubernetes command line client to utlize the created cluster.
https://github.com/GoogleCloudPlatform/kubernetes/releases

Grab the tarball and from the extracted release you can just directly use the
cli binary at ./kubernetes/platforms/linux/amd64/kubecfg

You'll need the address of the kubernetes master as environment variable :

    juju status kubernetes-master/0

Grab the public-address there and export it as KUBERNETES_MASTER environment
variable :

    export KUBERNETES_MASTER=$(juju status --format=oneline kubernetes-master | cut -d' ' -f3):8080

And now you can run through the kubernetes examples per normal. :

    $ kubecfg list minions

You can add capacity by adding more minions :
     $ juju add-unit flannel
     $ juju add-unit kubernetes --to # (the id that flannel is assigned)

Caveat
======

Kubernetes currently has several platform specific functionality. For example
load balancers and persistence volumes only work with the google compute
provider atm.

The juju integration uses the kubernetes null provider. This means external
load balancers and storage can't be directly driven through kubernetes config
files.
