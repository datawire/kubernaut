# Kubernaut

[![Join the chat at https://gitter.im/datawire/kubernaut](https://badges.gitter.im/datawire/kubernaut.svg)](https://gitter.im/datawire/kubernaut?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/datawire/kubernaut.svg?branch=master)](https://travis-ci.org/datawire/kubernaut)

Kubernaut provides on-demand, ephemeral Kubernetes clusters for development and testing.

Google Container Engine (and its brethren) are great if you need to spin up a cluster for a long-running job (e.g., your cloud service). But what if you want your CI system to run tests on a clean Kubernetes install? Or what if you want to reproduce a specific bug on a specific version of Kubernetes?

In these situations, you not only want an on-demand cluster -- you want it to go away when you're done.

# Installation

## macOS

Kubernaut is in early development and we have not finished the macOS installation process. [Issue #3 (GH-3)](../../issues/3) exists to track progress. In the meantime the recommended way to install Kubernaut on macOS is via `pip`.

```bash
$ brew install python3
$ pip3 install kubernaut
```

## Fedora 25 or later

```bash
$ curl -s https://packagecloud.io/install/repositories/datawireio/stable/script.rpm.sh | sudo bash
$ sudo dnf install kubernaut
```

## Ubuntu 16.04 or later

```bash
$ curl -s https://packagecloud.io/install/repositories/datawireio/stable/script.deb.sh | sudo bash
$ sudo apt install kubernaut
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

# Feature Requests and Bug Reports

We are open to suggestions about new and exciting features along with receiving bug reports. You can report feature requests for either the CLI app or the [kubernaut.io](https://github.com/datawire/kubernaut) service in this repository.

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

# Upgrades

## macOS

```bash
$ pip3 install -U kubernaut
```

## Fedora 25 or later

```bash
$ sudo dnf upgrade kubernaut
```

## Ubuntu 16.04 or later

```bash
$ sudo apt-get update && apt-get install kubernaut
```

# Examples

## Travis CI

Examples of using Kubernaut from a [Travis-CI](https://travis-ci.org) build can be found in the [examples/travis-ci](examples/travis-ci) directory.

# Known Limitations

Nothing is perfect. Below are some known limitations.

## LoadBalancer service is stuck in "Pending" state.

Kubernaut does not currently support LoadBalancer (`type: LoadBalancer`) services. If this feature is important to you please comment or vote in [Issue #4 (GH-4)](../../issues/4). You can use [Telepresence](https://www.telepresence.io) to run a local shell to connect to services on your cluster.

# Usage Reporting

Kubernaut collects some basic information about its users so it can send important client notices such as new version availability and security bulletins. We also use the information to anonymously aggregate basic usage analytics.

## Why?

- We want to know how you are using our software, so we can make it better for you. Knowing what versions are being used, in aggregate, is very helpful for development and testing.
- We ship new releases frequently, with new features and bug fixes. We want you to know when we ship a new release.

## What is collected?

The following information is collected and sent during version checks:

- Application Name ("kubernaut")
- Application Version
- Install Identifier (locally generated for only Kubernaut and stored in `${HOME}/.config/kubernaut/id`)
- Platform Information (Operating System, Python version)

The reporting code can be found in [datawire/scout.py](https://github.com/datawire/scout.py).

## When is it collected?

We collect information during software version checks. We check versions during any command invocation.

## Can it be disabled?

Yes! Set an environment variable `SCOUT_DISABLE=1`.

# License

Licensed under Apache 2.0. Please read [LICENSE](LICENSE) for details.
