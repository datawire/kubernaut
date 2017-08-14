# Kubernaut

Kubernaut provides on-demand, ephemeral Kubernetes clusters for development and testing.

Google Container Engine (and its brethren) are great if you need to spin up a cluster for a long-running job (e.g., your cloud service). But what if you want your CI system to run tests on a clean Kubernetes install? Or what if you want to reproduce a specific bug on a specific version of Kubernetes?

In these situations, you not only want an on-demand cluster -- you want it to go away when you're done.

# Installation

## macOS

```bash
brew cask install datawire/blackbird/kubernaut
```

## Fedora 25 or later

```bash
curl -s https://packagecloud.io/install/repositories/datawireio/kubernaut/script.rpm.sh | sudo bash
sudo dnf install kubernaut
```

## Ubuntu 16.04 or later

```bash
curl -s https://packagecloud.io/install/repositories/datawireio/kubernaut/script.deb.sh | sudo bash
sudo apt install --no-install-recommends kubernaut
```

# Quick Start

1. Get your Kubernaut access token with `kubernaut get-token`.
2. Set your Kubernaut access token with `kubernaut set-token <TOKEN>`.
3. Claim your Kubernetes cluster with `kubernaut claim`
4. Use your Kubernetes cluster:

    ```bash
    export KUBECONFIG=${HOME}/.kube/kubernaut
    kubectl cluster-info

    Kubernetes master is running at https://i-abcxyz.kubernaut.io:6443
    KubeDNS is running at https://i-abcxyz.kubernaut.io:6443/api/v1/proxy/namespaces/kube-system/services/kube-dns

    To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
    ```

5. When you are all done use `kubernaut discard` to release the cluster or if you are lazy and forget about it then the cluster will be automatically terminated after 60 minutes.

# Command Reference

The command `kubernaut --help` prints the below help table:

```bash
$> kubernaut --help
Usage: kubernaut [OPTIONS] COMMAND [ARGS]...

  kubernaut: easy kubernetes clusters for painless development and testing

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  claim       Claim a Kubernetes cluster
  discard     Discard a previously claimed Kubernetes
  get-token   Retrieve a token to use the Kubernaut service
  kubeconfig  Get a clusters kubeconfig
  set-token   Set a token to use the Kubernaut service
```

# License

Licensed under Apache 2.0. Please read [LICENSE](LICENSE) for details.
