# Kubernaut

Kubernaut provides on-demand, ephemeral Kubernetes clusters for development and testing.

Google Container Engine (and its brethren) are great if you need to spin up a cluster for a long-running job (e.g., your cloud service). But what if you want your CI system to run tests on a clean Kubernetes install? Or what if you want to reproduce a specific bug on a specific version of Kubernetes?

In these situations, you not only want an on-demand cluster -- you want it to go away when you're done.

# Getting Started

Install the `kubernaut` tool to register and use the service.

## Pre-Release Install Instructions

Requires Python 3!

```bash
# only need these two commands during development
$ virtualenv venv --python python3
$ source venv/bin/activate

$ pip install git+https://github.com/datawire/kubernaut.git
```

# Quick Start

1. Login to the service `kubernaut login` (ask Phil for the development password)

2. Claim a new Kubernetes cluster with `kubernaut claim`. Claimed clusters are ephemeral and terminated automatically after 60 minutes.

3. Start using your cluster!

    ```bash
    $ export KUBECONFIG=$(kubernaut kubeconfig -p)
    $ kubectl cluster-info

    Kubernetes master is running at https://i-0c70e14cbaec71ddf.kubernaut.io:6443
    KubeDNS is running at https://i-0c70e14cbaec71ddf.kubernaut.io:6443/api/v1/proxy/namespaces/kube-system/services/kube-dns

    To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
    ```

# License

Licensed under Apache 2.0. Please read [LICENSE](LICENSE) for details.
