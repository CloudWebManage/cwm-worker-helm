# cwm-worker-helm

Automatically updated repository for packaged Helm charts 

## Using a chart from the repository

Choose a chart from the sub-directories of this repository and set in env var

```
CHART_NAME=cwm-worker-ingress
```

Add the repo

```
helm repo add "${CHART_NAME}" "https://raw.githubusercontent.com/CloudWebManage/cwm-worker-helm/master/${CHART_NAME}"
```

Deploy a version of the chart (replace VERSION and RELEASE_NAME)

```
helm upgrade --install --version VERSION RELEASE_NAME ${CHART_NAME} 
```

## Adding a chart version

The following examples adds a version for the cwm-worker-ingress helm chart.

It assumes the following directory structure:

```
|- cwm-worker-ingress
    |- helm: the source helm chart
|- cwm-worker-helm: the packaged charts repository
```

Install Helm

```
curl -Ls https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz -ohelm.tar.gz &&\
tar -xzvf helm.tar.gz && sudo mv linux-amd64/helm /usr/local/bin/helm &&\
sudo chmod +x /usr/local/bin/helm &&\
rm -rf linux-amd64 && rm helm.tar.gz &&\
helm version
```

Change directory to the packaged charts repository (this repository)

Set the package version in env var, you can use one of the following

* tagged version: `VERSION=0.1.2`
* github sha: `VERSION=0.0.0-${GITHUB_SHA}`

Set the source and target directories

```
SOURCE_DIR=../cwm-worker-ingress/helm
TARGET_DIR=cwm-worker-ingress
```

Package the chart

```
helm package "${SOURCE_DIR}" --version "${VERSION}" --destination "${TARGET_DIR}"
```

Update the repo index

```
helm repo index \
    --url "https://raw.githubusercontent.com/CloudWebManage/cwm-worker-helm/master/${TARGET_DIR}/" \
    "${TARGET_DIR}"
```
