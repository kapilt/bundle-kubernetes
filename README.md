# kubernetes-bundle


Kubernetes is an open source system for managing containerized applications.
Kubernetes uses [Docker](http://docker.com) to package, instantiate, and run
containerized applications.

[Juju](https://juju.ubuntu.com) is an open source cloud orchestration and
provisioning system that works with many different cloud environments.
The kubernetes-bundle allows you to deploy the many services of Kubernetes to a
cloud environment and get started using the Kubernetes technology quickly.


## Components of Kubernetes

### Kubernetes master
The controlling unit in a Kubernetes cluster is called the master.  It is the
main management contact point providing many management services for the worker
nodes.

### Kubernetes minion
The servers that perform the work are known as minions.  Minions must be able to
communicate with the master and run the workloads that are assigned to them.

### Flannel
Flannel is a [software defined networking](http://en.wikipedia.org/wiki/Software-defined_networking) component that provides individual subnets for each machine in the cluster.

### etcd
Etcd is an open source key-value configuration store that Kubernetes uses to
persist master state, and Flannel consumes to coordinate subnets among units.

## Usage

#### Juju Quickstart
You will need to [install the Juju client](https://juju.ubuntu.com/install/) and
`juju-quickstart` as pre-requisites.  To deploy the bundle use `juju-quickstart`
which runs on Mac OS (`brew install juju-quickstart`) or Ubuntu
(`apt-get install juju-quickstart`).

#### For further information on getting started with Juju

Juju has complete documentation with regard to setup, and cloud configuration
on it's own [documentation site](https://juju.ubuntu.com/docs/).

- [Getting Started](https://juju.ubuntu.com/docs/getting-started.html)
- [Using Juju](https://juju.ubuntu.com/docs/charms.html)

### Bundle Usage

This bundle can be used to deploy Kubernetes onto any cloud it can be
orchestrated directly in the Juju Graphical User Interface, when using
`juju quickstart`:

    juju quickstart https://raw.githubusercontent.com/whitmo/bundle-kubernetes/master/bundles.yaml
    juju expose kubernetes-master


The command above will do a few things on behalf of the user:

- Inspect for a bootstrapped environment, and bootstrap if required
- Deploy the Juju GUI to the topology, co-located on the bootstrap node
- Provision 4 machines, and deploy the Kubernetes services on top of them (etcd,
  Kubernetes-master, two Kubernetes minions using flannel)
- Orchestrate the relations among the services, and exit.

For further reading on [Juju Quickstart](https://pypi.python.org/pypi/juju-quickstart)

# Using the Kubernetes Client

You'll need the Kubernetes command line client,
[kubectl](https://github.com/GoogleCloudPlatform/kubernetes/blob/master/docs/kubectl.md)
to interact with the created cluster.  The kubectl command is installed on the
kubernetes-master charm, but if you want to work with the cluster from your
computer you will need to install the binary locally.

Download the Kuberentes release from:
https://github.com/GoogleCloudPlatform/kubernetes/releases
and extract the release, you can then just directly use the cli binary at
./kubernetes/platforms/linux/amd64/kubectl

You'll need the address of the kubernetes-master as environment variable :

    juju status kubernetes-master/0

Grab the public-address there and export it as KUBERNETES_MASTER environment
variable :

    export KUBERNETES_MASTER=$(juju status --format=oneline kubernetes-master | cut -d' ' -f3):8080

And now you can run kubectl on the command line :

    $ kubectl get mi

See the [kubectl documentation](https://github.com/GoogleCloudPlatform/kubernetes/blob/master/docs/kubectl.md)
for more details of what can be done with the command line tool.

### Scaling up the cluster

You can add capacity by adding more flannel units and Kubernetes minions:

     juju add-unit flannel
     juju add-unit kubernetes --to # (the id that flannel is assigned)

## Known Limitations

Kubernetes currently has several platform specific functionality. For example
load balancers and persistence volumes only work with the Google Compute
provider at this time.

The Juju integration uses the Kubernetes null provider. This means external
load balancers and storage can't be directly driven through Kubernetes config
files.

## How to contribute

The kubernetes-bundle is open source and available on github.com.  If you want
to get started developing on the bundle you can clone it from github.  Often
you will need the related charms which are also on github.

    mkdir ~/bundles
    git clone https://github.com/whitmo/kubernetes-bundle.git ~/bundles/kubernetes-bundle
    mkdir -p ~/charms/trusty
    git clone https://github.com/whitmo/kubernetes-charm.git ~/charms/trusty/kubernetes
    git clone https://github.com/whitmo/kubernetes-master-charm.git ~/charms/trusty/kubernetes-master
    git clone https://github.com/whitmo/etcd-charm.git ~/charms/trusty/etcd-charm
    git clone https://github.com/whitmo/flannel-charm.git ~/charms/trusty/flannel-charm

    juju quickstart specs/develop.yaml
    juju expose kubernetes-master

## Current and Most Complete Information

  - [kubernetes-master charm on Github](https://github.com/whitmo/charm-kubernetes-master)
  - [kubernetes charm on GitHub](https://github.com/whitmo/charm-kubernetes)
  - [etcd charm on GitHub](https://github.com/whitmo/etcd-charm)
  - [Flannel charm on GitHub](https://github.com/whitmo/flannel-charm)

More information about the
[Kubernetes project](https://github.com/GoogleCloudPlatform/kubernetes) or check
out the [Kubernetes Documentation](https://github.com/GoogleCloudPlatform/kubernetes/tree/master/docs)
for more details about the Kubernetes concepts and terminology.

Having a problem? Check the [Kubernetes issues database](https://github.com/GoogleCloudPlatform/kubernetes/issues)
for related issues.
