# Kubernaut

[![Build Status](https://travis-ci.org/datawire/kubernaut.svg?branch=master)](https://travis-ci.org/datawire/kubernaut)

Ephemeral Kubernetes clusters for frustration and friction free development. This is the `kubernaut` CLI.

# Installation

An executable binary is provided for both Linux and MacOS. There is no Windows support at this time. 

## Native Installation

Latest release: `curl http://releases.datawire.io/kubernaut/latest.txt`

### Linux

`curl -OL http://releases.datawire.io/kubernaut/$(curl http://releases.datawire.io/kubernaut/latest.txt)/linux/amd64/kubernaut`

### macOS

`curl -OL http://releases.datawire.io/kubernaut/$(curl http://releases.datawire.io/kubernaut/latest.txt)/darwin/amd64/kubernaut`

# Quick Start

## Get Token

**NOTE**: This is temporary until we have a better account mgmt and login UX.

1. Goto https://kubernaut.io/token and login.
2. Copy the token to your clipboard.
3. Run the below command:

`kubernaut config backend create --url="https://next.kubernaut.io" --name="v2" --activate $TOKEN`

## Create a cluster claim

`kubernaut claims create --name mycluster`

## View active Claims

`kubernaut claims list`

## Delete a cluster claim

`kubernaut claims delete mycluster`

# Developer Information

## Versioning

The `kubernaut` command line application uses [Calendar Versioning ("CalVer")](https://calver.org/) for releases.

- The version scheme is `${YYYY}.${MM}.${DD}[-${GIT_COMMIT}]`.
- Latest releases always have the `${GIT_COMMIT}` appended after a dash.
- Latest releases are any build from `master` branch that passes CI tests. 
- **FUTURE** - Stable release cadence has not been determined but *WILL HAVE* the form `${YYYY}.${MM}.${DD}` without the `${GIT_COMMIT}` appended.
