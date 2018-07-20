# Using Kubernaut from Travis CI

Kubernaut is very easy to use from [Travis CI Free](https://travis-ci.org) or [Travis CI Pro](https://travis-ci.com).

This directory contains basic Travis-CI `.travis.yml` scripts you can use as a starting point for various languages. Depending on your language just copy one into your GitHub repository and then rename it to `.travis.yml`. You will also need to register your GitHub repository with Travis CI.

## Configuring Travis CI with your Kubernaut Token

To configure Travis CI to authenticate with Kubernaut you need to add an environment variable containing your token. Run the below command to get setup. Your Kubernaut token can found in a file on your local filesystem `~/.config/kubernaut/config.json`:

```bash
$> travis env set KUBERNAUT_TOKEN <TOKEN>
```
