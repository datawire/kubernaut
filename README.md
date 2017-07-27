# Kubernaut

Kubernetes clusters on-demand for painless development and testing.

# Getting Started

Install the `kubernaut` tool to register and use the service.

## Pre-Release Install Instructions

```bash
$ pip install git+https://github.com/datawire/kubernaut.git
```

# Quick Start

1. Register with the [kubernaut.io](https://kubernaut.io) community using `kubernaut register`.

2. Claim a new Kubernetes cluster with `kubernetes claim`. Claimed clusters are ephemeral and terminated automatically after 60 minutes.

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
